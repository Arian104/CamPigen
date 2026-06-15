"use client";

import { EmailBlock } from "./types";
import { BLOCK_REGISTRY } from "./blockRegistry";
import { SettingsGroup } from "./PropertyControls";
import styles from "./EmailBuilder.module.css";

type Props = {
  block: EmailBlock | null;
  onUpdateBlock: (block: EmailBlock) => void;
};

function updateProp(
  block: EmailBlock,
  key: string,
  value: string,
  onUpdateBlock: (block: EmailBlock) => void,
) {
  onUpdateBlock({
    ...block,
    props: {
      ...block.props,
      [key]: value,
    },
  });
}

export function PropertyPanel({ block, onUpdateBlock }: Props) {
  if (!block) {
    return (
      <aside className={`${styles.propertyPanel} propertyPanel`}>
        <h3>Properties</h3>
        <p className="muted">Select a block to edit its settings.</p>
      </aside>
    );
  }

  const config = BLOCK_REGISTRY[block.type];

  const set = (key: string, value: string) =>
    updateProp(block, key, value, onUpdateBlock);

  return (
    <aside className={`${styles.propertyPanel} propertyPanel`}>
      <div className="propertyPanelHeader">
        <div>
          <h3>{config.label.toUpperCase()}</h3>
          <p className="muted">Customize selected block.</p>
        </div>

        <span className="blockSpanBadge">{block.span}/3</span>
      </div>

      <SettingsGroup title="Layout">
        <label className="builderField">
          <span>Column Width</span>
          <select
            value={block.span}
            onChange={(e) =>
              onUpdateBlock({
                ...block,
                span: Number(e.target.value) as 1 | 2 | 3,
              })
            }
          >
            <option value={1}>1 Column</option>
            <option value={2}>2 Columns</option>
            <option value={3}>Full Width</option>
          </select>
        </label>
      </SettingsGroup>

      <config.Properties block={block} set={set} />
    </aside>
  );
}
