Website Image Tags

website-image-tags

1793569513

Image tags and sizes used for link previews, favicons, and app icons.  Platforms change these limits without much notice, and some are not officially documented; these were last checked in November 2026.  Values marked with \* are from memory or third-party sources, and other values may also rely on secondary sources.

## Recommended

This set covers link previews, browser tabs, search results, and home screens on current platforms:

| File                     | Size      | Used for                                 |
|--------------------------|-----------|------------------------------------------|
| `preview.png`            | 1200x630  | Large link previews on social and chat apps |
| `favicon.ico`            | 32x32     | Older browsers and automated tools       |
| `icon.svg`               | Scalable  | Browser tabs                             |
| `apple-touch-icon.png`   | 180x180   | iOS home screen                          |
| `icon-192.png`           | 192x192   | Android home screen                      |
| `icon-512.png`           | 512x512   | Progressive web app install              |
| `icon-maskable-512.png`  | 512x512   | Android adaptive icons                   |

```html
<meta property="og:image" content="https://example.com/preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Description of the image">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

The `icons` section of `manifest.webmanifest` is below; web app install also needs `name` or `short_name`, `start_url`, and `display`:

```json
{
  "icons": [
    {"src": "/icon-192.png", "type": "image/png", "sizes": "192x192"},
    {"src": "/icon-512.png", "type": "image/png", "sizes": "512x512"},
    {"src": "/icon-maskable-512.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable"}
  ]
}
```

The 1200x630 image suits pages with a designed preview image, and fills the width of a message in chat apps.  If the only image is a logo or icon, use a 280x280 square image instead so it appears as a small thumbnail next to the title, set the `og:image:width` and `og:image:height` tags to match, and use `twitter:card` `summary`.  Do not reuse the 512x512 app icon for previews, since WhatsApp will show it at full size.

- Use absolute `https://` URLs for preview images
- Use PNG or JPEG for preview images, and keep important content centered in case of cropping
- Keep preview images under 600 KB, which is WhatsApp's documented limit
- Serve `favicon.ico` from the site root, since some tools only look there
- Give the Apple touch icon an opaque background and square corners
- Keep the logo in a maskable icon inside a centered circle with a radius of 40% of the icon width
- `sizes="32x32"` reportedly stops Chrome from preferring the ICO over the SVG
- Change the filename when replacing an image, since platforms and browsers cache them aggressively

## Exhaustive

### Link Previews

| Tag                                     | Used by                          | Size                             | Aspect ratio | File limit |
|-----------------------------------------|----------------------------------|----------------------------------|--------------|------------|
| `og:image`                              | Facebook                         | 1200x630 (600x315 for large, 200x200 minimum) | 1.91:1 | 8 MB |
| `og:image`                              | LinkedIn                         | 1200x627 minimum                 | 1.91:1       | 5 MB       |
| `og:image`                              | WhatsApp                         | 300 pixels wide or more for large | 4:1 or narrower | 600 KB   |
| `og:image`                              | Discord                          | 1200x630 in Discord's example; no size requirement | Undocumented | Undocumented |
| `og:image`                              | Signal                           | Any size meeting the rules below; 1200x630 and 280x280 work | See the rules below | Undocumented |
| `og:image`                              | Slack, iMessage, others          | 1200x630 for large\*, 280x280 for thumbnail\* | 1.91:1 for large\*, 1:1 for thumbnail\* | Undocumented |
| `twitter:image` (`summary_large_image`) | X/Twitter                        | 1200x600\* (300x157 minimum\*, 4096x4096 maximum\*) | 2:1\* | 5 MB\* |
| `twitter:image` (`summary`)             | X/Twitter                        | 400x400\* (144x144 minimum\*)    | 1:1\*        | 5 MB\*     |

X falls back to `og:image` when `twitter:image` is missing, but needs `twitter:card` to choose the card format.\*  X accepts JPG, PNG, WEBP, and GIF, and only uses the first frame of an animated GIF.\*

Chat apps choose between a large preview and a small thumbnail using either the image's dimensions or the page's tags:

| App             | Large preview when                                                       | Source                 |
|-----------------|--------------------------------------------------------------------------|------------------------|
| Discord         | `twitter:card` is `summary_large_image`                                  | [Documentation][discord] |
| WhatsApp        | At least 300 pixels wide, 4:1 or narrower, and under 600 KB              | [Documentation][whatsapp] |
| Slack           | About 400 pixels wide or more                                            | [One contributor's report][pr], not documented |
| Signal Desktop  | Width and height are at least 200 pixels, and not within 5% of square    | [Source code][signal-desktop] |
| Signal Android  | Width is at least 150dp in device pixels, and wider than tall            | [Source code][signal-android] |
| Signal iOS      | Width is at least about 2x the maximum message width, and height is at least 33% of that | [Source code][signal-ios] |

WhatsApp documents the requirements for a large preview, and says it may relax them or revert to small previews without giving a threshold, so a thumbnail under 300 pixels wide comes from the same [report][pr].  Signal does not use a single width threshold, so a large square image may still appear as a thumbnail.  Discord shows a small image beside the text by default, accepts PNG, GIF, JPEG, WEBP, and AVIF, and fetches the image to measure it unless `og:image:width` and `og:image:height` are set.

[discord]: https://docs.discord.com/developers/link-previews/overview
[whatsapp]: https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews/
[pr]: https://github.com/albertyw/chase-center-calendar/pull/64/files
[signal-desktop]: https://github.com/signalapp/Signal-Desktop/blob/5dad34ad5ea1a5b6229412e5c8ac0a696ff7532d/ts/linkPreviews/shouldUseFullSizeLinkPreviewImage.std.ts
[signal-android]: https://github.com/signalapp/Signal-Android/blob/515db93fb48206d63406cbfb48c5816f6af1d9e2/app/src/main/java/org/thoughtcrime/securesms/util/MessageRecordUtil.kt
[signal-ios]: https://github.com/signalapp/Signal-iOS/blob/b6beaf01029a239df6b9b300c3524389a1b8bca3/Signal/ConversationView/CellViews/CVLinkPreviewView.swift

### Preview Image Properties

| Tag                     | Meaning                                  |
|-------------------------|------------------------------------------|
| `og:image:url`          | Same as `og:image`                       |
| `og:image:secure_url`   | HTTPS alternate URL                      |
| `og:image:type`         | MIME type                                |
| `og:image:width`        | Width in pixels                          |
| `og:image:height`       | Height in pixels                         |
| `og:image:alt`          | Description of the image                 |
| `twitter:image:alt`     | Description of the image, 420 characters maximum\* |

### Structured Data

| Tag                           | Used by         | Size                       | Aspect ratio                 |
|-------------------------------|-----------------|----------------------------|------------------------------|
| JSON-LD `image` on an Article | Google Search   | Width x height of at least 50,000 pixels | Provide 16:9, 4:3, and 1:1 |
| `<meta itemprop="image">`     | Schema.org microdata consumers | Same as `og:image`\* | 1.91:1\*         |

### Favicons

| Tag                                         | Size                     | Used by                              |
|---------------------------------------------|--------------------------|--------------------------------------|
| `<link rel="icon" type="image/svg+xml">`    | Scalable                 | Modern browsers, including Safari 26 and later |
| `<link rel="icon" type="image/png">`        | 16x16\*, 32x32\*         | Browser tabs                         |
| `<link rel="icon">` or `/favicon.ico`       | 16x16\*, 32x32\*, 48x48\* | Older browsers and automated tools   |
| `<link rel="icon">`                         | Square, above 48x48 (8x8 minimum) | Google Search results       |
| `<link rel="shortcut icon">`                | Same as `icon`           | Older alternative to `icon`          |

### App Icons

| Tag                                   | Size                                         | Used by                  |
|---------------------------------------|----------------------------------------------|--------------------------|
| `<link rel="apple-touch-icon">`       | 180x180                                      | Current iPhones\*        |
| `<link rel="apple-touch-icon">`       | 167x167                                      | iPad Pro\*               |
| `<link rel="apple-touch-icon">`       | 152x152                                      | iPad\*                   |
| `<link rel="apple-touch-icon">`       | 57x57\*, 60x60\*, 72x72\*, 76x76\*, 114x114\*, 120x120\*, 144x144\* | Older iOS devices |
| `/apple-touch-icon.png`               | 180x180                                      | Safari, without a `<link>` tag |
| Web manifest `icons`                  | 192x192, 512x512                             | Android, web app install |
| Web manifest `icons` with `maskable`  | 512x512                                      | Android adaptive icons   |

### Legacy

These are safe to skip on new sites:

| Tag                                      | Size                                 | Used by                             |
|------------------------------------------|--------------------------------------|-------------------------------------|
| `<link rel="image_src">`                 | Same as `og:image`\*                 | Older scrapers\*                    |
| `twitter:image:src`                      | Same as `twitter:image`\*            | Older name for `twitter:image`\*    |
| `<link rel="apple-touch-icon-precomposed">` | Same as `apple-touch-icon`\*      | iOS 6 and earlier                   |
| `<link rel="mask-icon">`                 | Scalable, single color SVG           | Safari pinned tabs before Safari 12\* |
| `<meta name="msapplication-TileImage">`  | 144x144\*                            | Windows 8 tiles\*                   |
| `browserconfig.xml`                      | 70x70\*, 150x150\*, 310x150\*, 310x310\* | Windows 8.1 and 10 tiles\*          |

Sources:

- [The Open Graph Protocol](https://ogp.me/)
- [Meta; Images in Link Shares](https://developers.facebook.com/docs/sharing/webmasters/images/)
- [LinkedIn; Make Your Website Shareable](https://www.linkedin.com/help/linkedin/answer/46687)
- [X; Summary Card with Large Image](https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image)
- [Discord; Link Previews](https://docs.discord.com/developers/link-previews/overview)
- [Google; Favicon in Search Results](https://developers.google.com/search/docs/appearance/favicon-in-search)
- [Google; Article Structured Data](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Evil Martians; How to Favicon](https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs)
- [Can I Use; SVG Favicons](https://caniuse.com/link-icon-svg)
- [Apple; Configuring Web Applications](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
- [web.dev; Maskable Icons](https://web.dev/articles/maskable-icon)
