```{=html}
<div class="student-project-grid">
<% for (const item of items) {
  if (!Array.isArray(item.students) || !item.students.length || item.students.some(s => typeof s !== 'string' || !s.trim())) throw new Error('Project students must be a nonempty list of names: ' + item.title);
  const thumbnail = item.thumbnail || 'images/placeholder.svg';
  if (!/^images\/[a-zA-Z0-9_./-]+\.(svg|png|jpe?g|webp)$/i.test(thumbnail) || thumbnail.includes('..')) throw new Error('Use a local images/ thumbnail: ' + item.title);
  if (item.thumbnail && !item.thumbnail_alt) throw new Error('Add thumbnail_alt for ' + item.title);
%>
<article class="student-project-card">
  <figure class="student-project-visual">
    <img src="student-projects/<%- thumbnail %>" alt="<%- item.thumbnail_alt || 'Abstract network illustration; project thumbnail forthcoming.' %>" width="1200" height="750" loading="lazy">
    <% if (item.thumbnail_credit) { %><figcaption><%- item.thumbnail_credit %></figcaption><% } %>
  </figure>
  <div class="student-project-copy">
    <h3><%- item.title %></h3>
    <p class="student-project-team"><%- item.students.join(' · ') %></p>
  </div>
</article>
<% } %>
</div>
<% if (!items.length) { %><p>Student projects will appear here. Start with the proposal template below.</p><% } %>
```
