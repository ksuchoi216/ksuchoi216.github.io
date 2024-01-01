---
title: "Markup: Title *with* **Markdown**"
# title: "Markup: Title with Special&nbsp;---&nbsp;Characters"
# excerpt: "This post has no body content and should be blank on the post's page."
# excerpt_separator: "<!--more-->"
image: 
  path: /images/so-simple-sample-image-3.jpg
  thumbnail: /images/so-simple-sample-image-3-400x200.jpg
  caption: "Photo from [WeGraphics](http://wegraphics.net/downloads/free-ultimate-blurred-background-pack/)"
categories:
  - sample
tags:
  - sample
# link: https://github.com
# hidden: true
last_modified_at: 2017-03-09T14:25:52-05:00
---
Nested and mixed lists are an interesting beast. It's a corner case to make sure that lists within lists do not break the ordered list numbering order and list styles go deep enough.

## Ordered list
1. ordered item
2. ordered item 
  * **unordered**
  * **unordered** 
    1. ordered item
    2. ordered item
3. ordered item
4. ordered item

## inline code
For example `2009-09-05-edge-case-no-yaml-title.md` becomes **Edge Case No Yaml Title**.

## unordered
A few things to check for:
  * Non-breaking text in the title should have no adverse effects on layout or functionality.
  * Check the browser window / tab title.


## code
```python
def print_out(string):
  print(string)
```

Plugins like [**jekyll-sitemap**](https://github.com/jekyll/jekyll-feed) use this field to add a `<lastmod>` tag your `sitemap.xml`.


## first chapter
<!--more-->


## Link

> Only one thing is impossible for God: To find any sense in any copyright law on the planet.
> 
> <cite><a href="http://www.brainyquote.com/quotes/quotes/m/marktwain163473.html">Mark Twain</a></cite>

Some [link](#) can also be shown.


## Youtube

{% include responsive-embed url="https://www.youtube-nocookie.com/embed/l2Of1-d5E5o?controls=0&amp;" %}

```html
{% raw %}{% include responsive-embed url="https://www.youtube.com/watch?v=-PVofD2A9t8" ratio="16:9" %}{% endraw %}
```

```html
<!-- 21:9 aspect ratio -->
<div class="responsive-embed responsive-embed-21by9">
  <iframe class="responsive-embed-item" src="..."></iframe>
</div>

<!-- 16:9 aspect ratio -->
<div class="responsive-embed responsive-embed-16by9">
  <iframe class="responsive-embed-item" src="..."></iframe>
</div>

<!-- 4:3 aspect ratio -->
<div class="responsive-embed responsive-embed-4by3">
  <iframe class="responsive-embed-item" src="..."></iframe>
</div>

<!-- 1:1 aspect ratio -->
<div class="responsive-embed responsive-embed-1by1">
  <iframe class="responsive-embed-item" src="..."></iframe>
</div>
```

## twitter embed


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Oh I dunno. It&#39;s probably been over 15 years since I smudged out a face with a pencil and kneaded eraser. <a href="https://twitter.com/hashtag/WIP?src=hash">#WIP</a> <a href="https://twitter.com/hashtag/Sktchy?src=hash">#Sktchy</a> <a href="https://t.co/PwqbMddyVK">pic.twitter.com/PwqbMddyVK</a></p>&mdash; Michael Rose (@mmistakes) <a href="https://twitter.com/mmistakes/status/826644109670612997">February 1, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

This post tests Twitter Embeds.


## future date

This post lives in the future and is dated {{ page.date | date: "%c" }}. It should only appear when Jekyll builds your project with the `--future` flag.

```bash
jekyll build --future
```

## layout
other post


