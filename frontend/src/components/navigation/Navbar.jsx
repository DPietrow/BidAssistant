import { theme } from "../../theme";

function Navbar({ activePage, onNavigate }) {
  const tabs = [
    {
      id: "opportunities",
      label: "Opportunities",
    },
    {
      id: "projects",
      label: "Projects",
    },
  ];

  return (
    <nav
      style={{
        position: "sticky",
        top: 0,
        zIndex: 1000,
        background: theme.background,
        borderBottom: `1px solid ${theme.border}`,
        padding: "18px 0",
        marginBottom: "40px",
      }}
    >
      <div
        style={{
          maxWidth: "1400px",
          margin: "0 auto",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {/* Logo */}

        <div>
          <h2
            style={{
              margin: 0,
              color: theme.text,
              fontWeight: 700,
              letterSpacing: "-0.5px",
            }}
          >
            ATHENA
          </h2>

          <div
            style={{
              color: theme.mutedText,
              fontSize: 13,
            }}
          >
            AI Procurement Intelligence
          </div>
        </div>

        {/* Navigation */}

        <div
          style={{
            display: "flex",
            gap: "36px",
          }}
        >
          {tabs.map((tab) => {
            const active = activePage === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => onNavigate(tab.id)}
                style={{
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",

                  color: active ? theme.primary : theme.mutedText,

                  fontSize: "16px",
                  fontWeight: active ? 600 : 500,

                  paddingBottom: "8px",

                  borderBottom: active
                    ? `2px solid ${theme.primary}`
                    : "2px solid transparent",

                  transition: "all .2s ease",
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Placeholder */}

        <div
          style={{
            width: 120,
            textAlign: "right",
            color: theme.mutedText,
            fontSize: 14,
          }}
        >
          Prototype
        </div>
      </div>
    </nav>
  );
}

export default Navbar;