# 3 places you can put styling

1. HTML tags (non-inline styles, non-tailwind this is useful for <h1>, <h2>, etc. With tailwind these all look the same, so just always use <div>)
2. CSS / inline styles. These either go in a `.css` file, or `style="..."`
3. tailwind classes. These go in `<div class="...">`. They do the thing as inline styles (mostly), but have different names for the css things. For example, `margin-top: 70px` is something like `mt-6` or something. It has niceities like `mx-3` which translates to `margin-left: 20px; margin-right: 20px` and crucially has `hover:` (hover effects), `dark:` (dark mode), `lg:` (desktop vs mobile)

Also, there's bootstrap, which has classes that do common kinds of things like cards. Bootstrap has notions of "cards", "headers", etc., whereas tailwind is just abbreviations for css. Tailwind is 1:1 with CSS commands, whereas Bootstrap is trying to give you higher level concepts that aren't in CSS.