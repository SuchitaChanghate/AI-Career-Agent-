function Navbar({ activePage, setActivePage }) {

  const navigationItems = [
    {
      id: "dashboard",
      icon: "⌂",
      label: "Dashboard"
    },
    {
      id: "resume",
      icon: "▣",
      label: "Resume"
    },
    {
      id: "jobs",
      icon: "◎",
      label: "Job Match"
    },
    {
      id: "interview",
      icon: "◌",
      label: "Interview"
    }
  ];


  return (
    <aside className="sidebar">

      {/* Logo */}

      <div className="sidebar-logo">

        <div className="logo-mark">
          ✦
        </div>

        <div>

          <h2>
            AI Career
          </h2>

          <span>
            AGENT
          </span>

        </div>

      </div>


      {/* Navigation */}

      <div className="sidebar-navigation">

        <p className="navigation-title">
          WORKSPACE
        </p>


        {navigationItems.map((item) => (

          <button
            key={item.id}
            className={
              activePage === item.id
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setActivePage(item.id)}
          >

            <span className="nav-icon">
              {item.icon}
            </span>

            <span>
              {item.label}
            </span>

          </button>

        ))}

      </div>


      {/* Bottom Agent Status */}

      <div className="sidebar-bottom">

        <div className="agent-status">

          <div className="agent-status-icon">
            ✦
          </div>

          <div>

            <strong>
              AI Agent
            </strong>

            <span>
              <i></i>
              Online
            </span>

          </div>

        </div>


        <p>
          Your personal career intelligence
          workspace.
        </p>

      </div>

    </aside>
  );
}


export default Navbar;