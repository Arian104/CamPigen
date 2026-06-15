"use client";

import { useState } from "react";
import { ContactList, Tag } from "./types";

type Props = {
  selectedIds: string[];
  tags: Tag[];
  lists: ContactList[];
  loading: boolean;
  onBulkApply: (tagIds: string[], listIds: string[]) => Promise<void>;
  onClear: () => void;
};

export function BulkActionsBar({
  selectedIds,
  tags,
  lists,
  loading,
  onBulkApply,
  onClear,
}: Props) {
  const [tagId, setTagId] = useState("");
  const [listId, setListId] = useState("");

  if (selectedIds.length === 0) return null;

  return (
    <div className="cdpBulkBar">
      <strong>{selectedIds.length} selected</strong>

      <select value={tagId} onChange={(e) => setTagId(e.target.value)}>
        <option value="">Apply tag</option>
        {tags.map((tag) => (
          <option key={tag.id} value={tag.id}>{tag.name}</option>
        ))}
      </select>

      <select value={listId} onChange={(e) => setListId(e.target.value)}>
        <option value="">Add to list</option>
        {lists.map((list) => (
          <option key={list.id} value={list.id}>{list.name}</option>
        ))}
      </select>

      <button
        type="button"
        disabled={loading || (!tagId && !listId)}
        onClick={() => onBulkApply(tagId ? [tagId] : [], listId ? [listId] : [])}
      >
        Apply
      </button>

      <button type="button" className="ghostButton" onClick={onClear}>
        Clear
      </button>
    </div>
  );
}
