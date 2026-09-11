import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const sourcePath = path.join(root, "lectures/07-transformer-architecture/index.qmd");
const cssPath = path.join(root, "lectures/07-transformer-architecture/slides.css");
const outputDir = path.join(root, "notes/07-transformer-architecture/images");
const source = fs.readFileSync(sourcePath, "utf8");
const css = fs.readFileSync(cssPath, "utf8");

const figures = {
  "position-signal": "Attention can rearrange—but cannot detect the rearrangement",
  "sinusoidal-position": "Encode position with waves at different frequencies",
  "ffn-network": "The feed-forward network is a familiar two-layer MLP",
  "layernorm-features": "LayerNorm controls each token’s feature scale",
  "add-and-norm": "The classical Transformer wraps each sublayer with Add & Norm",
  "decoder-stack": "A Transformer decoder repeats one complete block",
  "encoder-stack": "A Transformer encoder repeats one complete block",
  "cross-attention": "Cross-attention asks the source for what the decoder needs",
  "encoder-decoder": "Now connect the encoder and decoder",
};

fs.mkdirSync(outputDir, { recursive: true });

for (const [name, heading] of Object.entries(figures)) {
  const headingStart = source.indexOf(`## ${heading}`);
  if (headingStart < 0) throw new Error(`Missing heading: ${heading}`);
  const nextHeading = source.indexOf("\n## ", headingStart + 3);
  const section = source.slice(headingStart, nextHeading < 0 ? source.length : nextHeading);
  const match = section.match(/<svg\b[\s\S]*?<\/svg>/);
  if (!match) throw new Error(`Missing SVG under: ${heading}`);

  let svg = match[0]
    .replace(/\sclass="([^"]*)"/g, (_, classes) => {
      const kept = classes.split(/\s+/).filter((c) => c && c !== "fragment" && c !== "visible");
      return kept.length ? ` class="${kept.join(" ")}"` : "";
    })
    .replace(/\sdata-fragment-index="[^"]*"/g, "")
    .replace("<svg", `<svg xmlns="http://www.w3.org/2000/svg"`);

  const style = `<style><![CDATA[
:root { --navy:#17364a; --teal:#168b91; --coral:#ee6848; --gold:#d7a520; --muted:#687a82; --ink:#26343a; }
svg { background:#fbfaf7; font-family:"Noto Sans",Arial,sans-serif; }
${css}
.fragment { visibility:visible !important; opacity:1 !important; }
]]></style>`;
  svg = svg.replace(/(<svg[^>]*>)/, `$1\n${style}\n<rect width="100%" height="100%" fill="#fbfaf7"/>`);
  fs.writeFileSync(path.join(outputDir, `${name}.svg`), svg);
}
