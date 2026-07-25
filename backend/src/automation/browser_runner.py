from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urljoin

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from src.models.automation_target import AutomationTargetRecord
from src.models.base import (
    DesiredState,
    FailureStep,
    RunStatus,
    ToggleAction,
    ToggleObservedState,
    ToggleVerificationMethod,
)


@dataclass(slots=True)
class CapturedValue:
    key: str
    selector: str
    value: str


@dataclass(slots=True)
class ToggleOutcome:
    state_before: ToggleObservedState
    state_after: ToggleObservedState
    action_taken: ToggleAction
    verification_method: ToggleVerificationMethod
    verified: bool


@dataclass(slots=True)
class BrowserRunResult:
    status: RunStatus
    captured_items: list[CapturedValue] = field(default_factory=list)
    toggle_result: ToggleOutcome | None = None
    failure_step: FailureStep | None = None
    failure_message: str | None = None


class BrowserRunner:
    async def execute(self, target: AutomationTargetRecord, requested_state: DesiredState) -> BrowserRunResult:
        if target.page_path:
            target_url = urljoin(f"{target.base_url.rstrip('/')}/", target.page_path.lstrip('/'))
        else:
            target_url = target.base_url
        toggle_rule = target.toggle_rule
        verification_method = ToggleVerificationMethod(toggle_rule["verificationMethod"])

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(target_url, wait_until="domcontentloaded", timeout=20000)

                captured_values: list[CapturedValue] = []
                for rule in target.extraction_rules:
                    locator = page.locator(rule["selector"]).first
                    value = (await locator.inner_text(timeout=5000)).strip()
                    captured_values.append(
                        CapturedValue(key=rule["key"], selector=rule["selector"], value=value)
                    )

                state_before = await self._detect_state(page, toggle_rule["stateSelector"], verification_method)
                if state_before == self._to_observed_state(requested_state):
                    await browser.close()
                    return BrowserRunResult(
                        status=RunStatus.NO_CHANGE_NEEDED,
                        captured_items=captured_values,
                        toggle_result=ToggleOutcome(
                            state_before=state_before,
                            state_after=state_before,
                            action_taken=ToggleAction.NONE,
                            verification_method=verification_method,
                            verified=True,
                        ),
                    )

                await page.locator(toggle_rule["controlSelector"]).first.click(timeout=5000)
                state_after = await self._detect_state(page, toggle_rule["stateSelector"], verification_method)
                action_taken = ToggleAction.TOGGLE_ONCE

                if state_after != self._to_observed_state(requested_state):
                    await page.locator(toggle_rule["controlSelector"]).first.click(timeout=5000)
                    state_after = await self._detect_state(page, toggle_rule["stateSelector"], verification_method)
                    action_taken = ToggleAction.RETRY_TOGGLE

                await browser.close()

                if state_after != self._to_observed_state(requested_state):
                    return BrowserRunResult(
                        status=RunStatus.FAILED,
                        captured_items=captured_values,
                        toggle_result=ToggleOutcome(
                            state_before=state_before,
                            state_after=state_after,
                            action_taken=action_taken,
                            verification_method=verification_method,
                            verified=False,
                        ),
                        failure_step=FailureStep.VERIFY,
                        failure_message="Unable to verify requested state after toggle",
                    )

                return BrowserRunResult(
                    status=RunStatus.SUCCESS,
                    captured_items=captured_values,
                    toggle_result=ToggleOutcome(
                        state_before=state_before,
                        state_after=state_after,
                        action_taken=action_taken,
                        verification_method=verification_method,
                        verified=True,
                    ),
                )
        except PlaywrightTimeoutError as exc:
            return BrowserRunResult(
                status=RunStatus.FAILED,
                failure_step=FailureStep.NAVIGATE,
                failure_message=f"Timed out during browser automation: {exc}",
            )
        except Exception as exc:
            return BrowserRunResult(
                status=RunStatus.FAILED,
                failure_step=FailureStep.TOGGLE,
                failure_message=f"Browser automation failed: {exc}",
            )

    async def _detect_state(
        self,
        page,
        selector: str,
        method: ToggleVerificationMethod,
    ) -> ToggleObservedState:
        node = page.locator(selector).first

        if method == ToggleVerificationMethod.ARIA_CHECKED:
            raw = (await node.get_attribute("aria-checked", timeout=5000) or "").strip().lower()
            if raw == "true":
                return ToggleObservedState.ON
            if raw == "false":
                return ToggleObservedState.OFF
            return ToggleObservedState.UNKNOWN

        if method == ToggleVerificationMethod.DOM_ATTRIBUTE:
            raw = (await node.get_attribute("data-state", timeout=5000) or "").strip().lower()
            if raw == "on":
                return ToggleObservedState.ON
            if raw == "off":
                return ToggleObservedState.OFF
            return ToggleObservedState.UNKNOWN

        text_value = (await node.inner_text(timeout=5000)).strip().lower()
        if "on" in text_value:
            return ToggleObservedState.ON
        if "off" in text_value:
            return ToggleObservedState.OFF
        return ToggleObservedState.UNKNOWN

    def _to_observed_state(self, desired_state: DesiredState) -> ToggleObservedState:
        return ToggleObservedState.ON if desired_state == DesiredState.ON else ToggleObservedState.OFF
