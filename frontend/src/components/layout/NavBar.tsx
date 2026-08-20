import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/targets", label: "Targets" },
  { to: "/runs", label: "Runs" },
  { to: "/history", label: "Run History" },
];

export function NavBar() {
  return (
    <nav className="nav-bar" aria-label="Main navigation">
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  );
}
