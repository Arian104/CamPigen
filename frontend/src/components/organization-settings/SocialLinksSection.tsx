"use client";

type OrganizationSocialFields = {
  facebook_url: string;
  instagram_url: string;
  linkedin_url: string;
  twitter_url: string;
  youtube_url: string;
  tiktok_url: string;
  whatsapp_number: string;
};

type Props = {
  organization: OrganizationSocialFields;
  updateField: <K extends keyof OrganizationSocialFields>(
    key: K,
    value: OrganizationSocialFields[K],
  ) => void;
};

export function SocialLinksSection({ organization, updateField }: Props) {
  return (
    <div>
      <h2>Social Links</h2>
      <p className="muted">
        These links are used by email footer/social blocks and campaign template variables.
      </p>

      <div className="formGrid">
        <label className="formField">
          <span>Facebook URL</span>
          <input
            value={organization.facebook_url}
            onChange={(e) => updateField("facebook_url", e.target.value)}
            placeholder="https://facebook.com/your-page"
          />
        </label>

        <label className="formField">
          <span>Instagram URL</span>
          <input
            value={organization.instagram_url}
            onChange={(e) => updateField("instagram_url", e.target.value)}
            placeholder="https://instagram.com/your-page"
          />
        </label>

        <label className="formField">
          <span>LinkedIn URL</span>
          <input
            value={organization.linkedin_url}
            onChange={(e) => updateField("linkedin_url", e.target.value)}
            placeholder="https://linkedin.com/company/your-company"
          />
        </label>

        <label className="formField">
          <span>Twitter/X URL</span>
          <input
            value={organization.twitter_url}
            onChange={(e) => updateField("twitter_url", e.target.value)}
            placeholder="https://x.com/your-page"
          />
        </label>

        <label className="formField">
          <span>YouTube URL</span>
          <input
            value={organization.youtube_url}
            onChange={(e) => updateField("youtube_url", e.target.value)}
            placeholder="https://youtube.com/@your-channel"
          />
        </label>

        <label className="formField">
          <span>TikTok URL</span>
          <input
            value={organization.tiktok_url}
            onChange={(e) => updateField("tiktok_url", e.target.value)}
            placeholder="https://tiktok.com/@your-page"
          />
        </label>

        <label className="formField">
          <span>WhatsApp Number / Link</span>
          <input
            value={organization.whatsapp_number}
            onChange={(e) => updateField("whatsapp_number", e.target.value)}
            placeholder="8801XXXXXXXXX or https://wa.me/8801XXXXXXXXX"
          />
        </label>
      </div>
    </div>
  );
}
