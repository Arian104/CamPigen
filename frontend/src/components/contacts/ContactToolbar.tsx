"use client";

type Tab = "directory" | "add" | "import" | "fields" | "tags" | "lists";

type Props = {
  activeTab: Tab;
  setActiveTab: (tab: Tab) => void;
  search: string;
  setSearch: (value: string) => void;
  message: string;
};

export function ContactToolbar({
  activeTab,
  setActiveTab,
  search,
  setSearch,
  message,
}: Props) {
  const tabs: { key: Tab; label: string }[] = [
    { key: "directory", label: "Directory" },
    { key: "add", label: "Add Contact" },
    { key: "import", label: "Import CSV" },
    { key: "fields", label: "Fields" },
    { key: "tags", label: "Tags" },
    { key: "lists", label: "Lists" },
  ];

  return (
    <section className="card">
      <div className="flexBetween">
        <div>
          <h1>Contacts CDP</h1>
          <p className="muted">
            Manage dynamic contacts, fields, tags, lists, and audience intelligence.
          </p>
          <p className="muted small">{message}</p>
        </div>

        <input
          className="cdpSearch"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search contacts..."
        />
      </div>

      <div className="cdpTabs">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            type="button"
            className={activeTab === tab.key ? "primaryButton" : "secondaryButton"}
            onClick={() => setActiveTab(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </section>
  );
}
