"use client";

type Props = {
  isCreating: boolean;
  loading: boolean;
  onCreate: () => void;
  onSave: () => void;
  onCancel: () => void;
};

export function TemplateSaveBar({
  isCreating,
  loading,
  onCreate,
  onSave,
  onCancel,
}: Props) {
  return (
    <div className="builderSaveBar">
      <div>
        <strong>{isCreating ? "Creating new template" : "Editing template"}</strong>
        <p className="muted">
          Changes are not saved until you click {isCreating ? "Create Template" : "Save Changes"}.
        </p>
      </div>

      <div className="actions">
        {isCreating ? (
          <button type="button" className="primaryButton" onClick={onCreate} disabled={loading}>
            Create Template
          </button>
        ) : (
          <button type="button" className="primaryButton" onClick={onSave} disabled={loading}>
            Save Changes
          </button>
        )}

        <button type="button" className="ghostButton" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
}
