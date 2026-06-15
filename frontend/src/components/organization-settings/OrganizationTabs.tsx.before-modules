"use client";

import { TABS, OrganizationTabKey } from "./tabs";

export function OrganizationTabs({
  activeTab,
  setActiveTab,
}: {
  activeTab: OrganizationTabKey;
  setActiveTab: (tab: OrganizationTabKey) => void;
}) {
  return (
    <aside className="orgTabs">
      {TABS.map((tab) => {
        const Icon = tab.icon;

        return (
          <button
            key={tab.key}
            type="button"
            className={activeTab === tab.key ? "orgTab active" : "orgTab"}
            onClick={() => setActiveTab(tab.key)}
          >
            <Icon size={18} />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </aside>
  );
}
