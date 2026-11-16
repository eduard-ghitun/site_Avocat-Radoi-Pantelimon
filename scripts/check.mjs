import { access, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pages, services } from '../src/content.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const dist = join(root, 'dist');
const posts = JSON.parse(await readFile(join(root, 'src', 'blog-posts.json'), 'utf8'));
const expected = [
  ...pages.map(page => join(dist, page.slug, 'index.html')),
  ...services.map(service => join(dist, 'servicii', service.slug, 'index.html')),
  ...posts.map(post => join(dist, 'blog', post.slug, 'index.html'))
];
for (const file of expected) {
  const html = await readFile(file, 'utf8');
  if (!html.includes('<html lang="ro">') || !html.includes('<main id="main">')) throw new Error(`Invalid page: ${file}`);
  for (const page of pages) {
    const href = page.slug ? `/${page.slug}/` : '/';
    if (!html.includes(`href="${href}"`)) throw new Error(`Missing navigation to ${href} in ${file}`);
  }
  if (!html.includes('href="mailto:avocat.pantelimon@gmail.com"') || !html.includes('id="mail-fallback"')) {
    throw new Error(`Email compose link or fallback options missing from ${file}`);
  }
}
const contactHtml = await readFile(join(dist, 'contact', 'index.html'), 'utf8');
if (!contactHtml.includes('maps.google.com/maps?q=44.4838785%2C26.1089708') || !contactHtml.includes('Pantelimon+R%C4%83doi')) {
  throw new Error('Contact page is missing the cabinet map or its Google Maps link');
}
for (const asset of ['styles.css', 'uikit.min.css', 'main.js', 'favicon.svg', 'og.svg', 'logo-radoi.svg', 'logo-radoi-dark.svg']) await access(join(dist, 'assets', asset));
if (!contactHtml.includes('class="uk-form-stacked"') || !contactHtml.includes('class="uk-input"') || !contactHtml.includes('class="uk-textarea"')) {
  throw new Error('Contact form is missing UIkit form components');
}
const homeHtml = await readFile(join(dist, 'index.html'), 'utf8');
if (!homeHtml.includes('href="/assets/uikit.min.css"') || !homeHtml.includes('class="service-card uk-card"')) {
  throw new Error('UIkit styles or card components are missing');
}
if (!homeHtml.includes('name="theme-color" content="#4b3428"')) {
  throw new Error('Browser theme color does not match the brown brand palette');
}
for (const asset of ['hero-radoi.png', 'home-radoi.png', 'about-radoi.png', 'services-radoi.png', 'contact-radoi.png']) await access(join(dist, 'assets', 'photos', asset));
await access(join(dist, 'sitemap.xml'));
await access(join(dist, 'robots.txt'));
console.log(`Checked ${expected.length} pages, navigation, and shared assets.`);
