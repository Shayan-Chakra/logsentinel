"""The dashboard web page (HTML, CSS and JavaScript in one text). Edit the look here."""

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LogSentinel</title>
<script>(function(){var t=null;try{t=localStorage.getItem("ls-theme")}catch(e){}
if(t!=="light"&&t!=="dark"){t=(window.matchMedia&&matchMedia("(prefers-color-scheme: light)").matches)?"light":"dark"}
document.documentElement.setAttribute("data-theme",t)})()</script>
<style>
  :root {
    --bg:#060912; --text:#e8ecf7; --muted:#8c97b2; --line:rgba(130,170,255,.16);
    --glass:rgba(16,24,46,.62); --cyan:#22d3ee; --violet:#8b5cf6; --pink:#ff3b6b;
    --CRITICAL:#ff3b6b; --HIGH:#ff8a3d; --MEDIUM:#fbbf24; --LOW:#34d399; --NONE:#22d3ee;
    --mono:ui-monospace,"Cascadia Code",Consolas,monospace;
    --top-bg:rgba(6,9,18,.72); --wash:rgba(255,255,255,.05); --wash2:rgba(255,255,255,.08); --btn-bg:rgba(255,255,255,.04);
    --field-bg:rgba(0,0,0,.28); --head:#c8d2ee; --primary-text:#04101a; --on-medium:#1b1300;
    --chip-bg:rgba(139,92,246,.16); --chip-line:rgba(139,92,246,.4); --chip-text:#cdbbff;
    --what-bg:rgba(139,92,246,.08); --what-line:rgba(139,92,246,.28); --what-title:#d9ccff;
    --todo-text:#d5dcf0; --warn-text:#ffe2b0; --cmd-bg:#04070f; --cmd-text:#9ff0ff;
    --tip-bg:rgba(10,15,30,.97); --panel-bg:rgba(10,15,30,.96); --toast-bg:rgba(16,24,46,.96);
    --scrim:rgba(2,4,10,.62); --shadow:rgba(0,0,0,.5);
    --grid:rgba(130,170,255,.10); --axis:rgba(130,170,255,.30); --rowline:rgba(130,170,255,.09);
    --series:#3987e5; --sevc-CRITICAL:#d03b3b; --sevc-HIGH:#ec835a; --sevc-MEDIUM:#fab219; --sevc-LOW:#0ca30c;
  }
  :root[data-theme="light"] {
    --bg:#f3f6fc; --text:#0f172a; --muted:#566280; --line:rgba(30,50,100,.16);
    --glass:rgba(255,255,255,.82); --cyan:#0e7490; --violet:#6d28d9; --pink:#be123c;
    --CRITICAL:#be123c; --HIGH:#c2410c; --MEDIUM:#a16207; --LOW:#15803d; --NONE:#0e7490;
    --top-bg:rgba(243,246,252,.82); --wash:rgba(15,23,42,.05); --wash2:rgba(15,23,42,.08); --btn-bg:rgba(15,23,42,.03);
    --field-bg:rgba(255,255,255,.9); --head:#243256; --primary-text:#ffffff; --on-medium:#ffffff;
    --chip-bg:rgba(109,40,217,.10); --chip-line:rgba(109,40,217,.35); --chip-text:#5b21b6;
    --what-bg:rgba(109,40,217,.06); --what-line:rgba(109,40,217,.25); --what-title:#4c1d95;
    --todo-text:#1e293b; --warn-text:#713f12; --cmd-bg:#0b1220; --cmd-text:#9ff0ff;
    --tip-bg:rgba(255,255,255,.98); --panel-bg:rgba(255,255,255,.98); --toast-bg:#ffffff;
    --scrim:rgba(15,23,42,.35); --shadow:rgba(15,23,42,.18);
    --grid:rgba(30,50,100,.10); --axis:rgba(30,50,100,.30); --rowline:rgba(30,50,100,.09);
    --series:#2a78d6; --sevc-CRITICAL:#d03b3b; --sevc-HIGH:#ec835a; --sevc-MEDIUM:#fab219; --sevc-LOW:#0ca30c;
  }
  * { box-sizing:border-box; }
  html { color-scheme:dark; }
  :root[data-theme="light"] { color-scheme:light; }
  body {
    margin:0; color:var(--text); background:var(--bg); min-height:100vh;
    font:15px/1.5 system-ui,"Segoe UI",Roboto,sans-serif;
  }
  .bg {
    position:fixed; inset:0; z-index:-1; pointer-events:none;
    background:
      radial-gradient(900px 500px at 12% -10%, rgba(34,211,238,.16), transparent 60%),
      radial-gradient(800px 500px at 100% 0%, rgba(139,92,246,.18), transparent 60%),
      linear-gradient(rgba(130,170,255,.05) 1px, transparent 1px) 0 0/44px 44px,
      linear-gradient(90deg, rgba(130,170,255,.05) 1px, transparent 1px) 0 0/44px 44px;
  }
  /* ---------- top bar ---------- */
  .top {
    position:sticky; top:0; z-index:5; display:flex; align-items:center; justify-content:space-between;
    flex-wrap:wrap; gap:12px; padding:14px 28px;
    background:var(--top-bg); backdrop-filter:blur(14px); border-bottom:1px solid var(--line);
  }
  .brand { display:flex; align-items:center; gap:12px; }
  .brand h1 {
    margin:0; font-size:21px; letter-spacing:.5px;
    background:linear-gradient(90deg,var(--cyan),var(--violet)); -webkit-background-clip:text; background-clip:text; color:transparent;
  }
  .sub { color:var(--muted); font-size:12px; letter-spacing:1.6px; text-transform:uppercase; }
  .top-actions { display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
  .pill { display:inline-flex; align-items:center; gap:7px; font-size:11px; font-weight:700; letter-spacing:1.5px;
          color:var(--LOW); border:1px solid color-mix(in srgb,var(--LOW) 45%,transparent); border-radius:999px; padding:3px 10px; }
  .pill i { width:8px; height:8px; border-radius:50%; background:var(--LOW); box-shadow:0 0 10px var(--LOW); animation:pulse 1.8s infinite; }
  .pill.off { color:var(--muted); border-color:var(--line); }
  .pill.off i { background:var(--muted); box-shadow:none; animation:none; }
  .muted { color:var(--muted); font-size:13px; }
  .btns { display:flex; gap:8px; flex-wrap:wrap; }
  .btn {
    font:600 13px system-ui,sans-serif; color:var(--text); text-decoration:none; cursor:pointer;
    padding:8px 14px; border-radius:10px; border:1px solid var(--line); background:var(--btn-bg);
    transition:.2s;
  }
  .btn:hover { border-color:var(--cyan); box-shadow:0 0 16px rgba(34,211,238,.25); transform:translateY(-1px); }
  .btn.primary { border:0; color:var(--primary-text); background:linear-gradient(90deg,var(--cyan),var(--violet)); box-shadow:0 0 18px rgba(34,211,238,.35); }
  .btn.primary:hover { box-shadow:0 0 28px rgba(139,92,246,.6); }
  .btn:disabled { opacity:.55; cursor:default; transform:none; box-shadow:none; }

  main { max-width:1180px; margin:0 auto; padding:26px 28px 40px; }
  h2 { display:flex; align-items:baseline; gap:10px; margin:34px 0 14px; font-size:15px; letter-spacing:2px; text-transform:uppercase; color:var(--head); }
  h2 small { color:var(--muted); font-size:12px; letter-spacing:.5px; text-transform:none; }
  h2::before { content:""; width:4px; height:16px; border-radius:2px; background:linear-gradient(var(--cyan),var(--violet)); align-self:center; }

  .glass { background:var(--glass); border:1px solid var(--line); border-radius:16px; backdrop-filter:blur(10px); }

  /* ---------- threat banner ---------- */
  .threat { --c:var(--NONE); display:flex; align-items:center; gap:18px; padding:20px 24px; margin-bottom:18px;
            border-color:color-mix(in srgb,var(--c) 45%,transparent); box-shadow:0 0 40px color-mix(in srgb,var(--c) 18%,transparent) inset, 0 0 30px color-mix(in srgb,var(--c) 14%,transparent); }
  .threat .dot { width:14px; height:14px; border-radius:50%; background:var(--c); box-shadow:0 0 18px var(--c); animation:pulse 1.8s infinite; flex:none; }
  .threat .label { font-size:12px; letter-spacing:2.4px; color:var(--muted); text-transform:uppercase; }
  .threat .level { font-size:26px; font-weight:800; letter-spacing:2px; color:var(--c); text-shadow:0 0 22px color-mix(in srgb,var(--c) 60%,transparent); }
  .threat .why { color:var(--muted); margin-left:auto; text-align:right; max-width:420px; font-size:13px; }

  /* ---------- notes ---------- */
  .note { display:flex; gap:12px; padding:14px 18px; margin-bottom:10px; line-height:1.55; font-size:14px;
          border-left:3px solid var(--MEDIUM); }
  .note::before { content:"i"; flex:none; width:22px; height:22px; border-radius:50%; display:grid; place-items:center;
                  font:700 13px serif; font-style:italic; color:var(--on-medium); background:var(--MEDIUM); }
  .note.demo { border-left-color:var(--violet); } .note.demo::before { background:var(--violet); color:#fff; }

  /* ---------- KPI cards ---------- */
  .kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; margin-top:16px; }
  .kpi { padding:18px 20px; transition:.25s; position:relative; overflow:hidden; }
  .kpi:hover { transform:translateY(-3px); border-color:rgba(34,211,238,.5); box-shadow:0 8px 30px rgba(34,211,238,.12); }
  .kpi .num { font-size:34px; font-weight:800; line-height:1.1; font-variant-numeric:tabular-nums; }
  .kpi .lab { color:var(--muted); font-size:12px; letter-spacing:1.4px; text-transform:uppercase; margin-top:4px; }
  .kpi::after { content:""; position:absolute; right:-30px; top:-30px; width:90px; height:90px; border-radius:50%;
                background:radial-gradient(circle,rgba(139,92,246,.35),transparent 70%); }

  /* ---------- incident cards ---------- */
  .cases { display:grid; grid-template-columns:repeat(auto-fill,minmax(330px,1fr)); gap:14px; }
  .case { --c:var(--NONE); padding:18px; display:grid; grid-template-columns:72px 1fr; gap:16px; transition:.25s;
          border-color:color-mix(in srgb,var(--c) 30%,transparent); }
  .case:hover { transform:translateY(-3px); box-shadow:0 10px 34px color-mix(in srgb,var(--c) 22%,transparent); }
  .sev-CRITICAL { --c:var(--CRITICAL); } .sev-HIGH { --c:var(--HIGH); } .sev-MEDIUM { --c:var(--MEDIUM); } .sev-LOW { --c:var(--LOW); }
  .ring { position:relative; width:72px; height:72px; }
  .ring svg { width:72px; height:72px; transform:rotate(-90deg); }
  .ring .track { stroke:var(--wash2); } .ring .bar { stroke:var(--c); filter:drop-shadow(0 0 5px var(--c)); transition:stroke-dasharray .8s; }
  .ring b { position:absolute; inset:0; display:grid; place-items:center; font-size:19px; font-weight:800; }
  .case .ip { font:700 16px var(--mono); }
  .tag { display:inline-block; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; letter-spacing:1.2px;
         color:var(--c); background:color-mix(in srgb,var(--c) 16%,transparent); border:1px solid color-mix(in srgb,var(--c) 45%,transparent); }
  .case .meta { color:var(--muted); font-size:12.5px; margin-top:6px; }
  .chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }
  .chip { font-size:11px; padding:2px 8px; border-radius:999px; background:var(--chip-bg); border:1px solid var(--chip-line); color:var(--chip-text); }
  .copy { margin-left:8px; font-size:11px; padding:1px 8px; border-radius:6px; cursor:pointer; color:var(--muted); background:none; border:1px solid var(--line); }
  .copy:hover { color:var(--cyan); border-color:var(--cyan); }

  /* ---------- tabs, search, filters ---------- */
  .tabs { display:flex; gap:6px; margin:30px 0 14px; flex-wrap:wrap; border-bottom:1px solid var(--line); }
  .tab { font:700 13px system-ui,sans-serif; letter-spacing:1.4px; text-transform:uppercase; color:var(--muted);
         background:none; border:0; padding:12px 18px; cursor:pointer; position:relative; transition:.2s; }
  .tab:hover { color:var(--text); }
  .tab.on { color:var(--cyan); }
  .tab.on::after { content:""; position:absolute; left:10px; right:10px; bottom:-1px; height:2px; border-radius:2px;
                   background:linear-gradient(90deg,var(--cyan),var(--violet)); box-shadow:0 0 12px var(--cyan); }
  .tab em { font-style:normal; margin-left:6px; font-size:11px; padding:1px 7px; border-radius:999px; background:var(--wash2); }
  .toolbar { display:flex; align-items:center; gap:12px; flex-wrap:wrap; padding:12px 14px; margin-bottom:16px; }
  .toolbar input { flex:1 1 240px; min-width:0; font:14px system-ui,sans-serif; color:var(--text); background:var(--field-bg);
                   border:1px solid var(--line); border-radius:10px; padding:9px 14px; outline:none; transition:.2s; }
  .toolbar input:focus { border-color:var(--cyan); box-shadow:0 0 14px rgba(34,211,238,.25); }
  .filters { display:flex; gap:6px; flex-wrap:wrap; }
  .fchip { --c:var(--cyan); font:600 12px system-ui,sans-serif; cursor:pointer; color:var(--muted); background:none;
           border:1px solid var(--line); border-radius:999px; padding:5px 12px; transition:.2s; }
  .fchip:hover { color:var(--text); border-color:var(--c); }
  .fchip.on { color:var(--c); border-color:var(--c); background:color-mix(in srgb,var(--c) 14%,transparent); box-shadow:0 0 12px color-mix(in srgb,var(--c) 30%,transparent); }
  .toolbar .muted { margin-left:auto; }
  .kbd { font:11px var(--mono); border:1px solid var(--line); border-radius:5px; padding:0 5px; color:var(--muted); }
  th.sortable { cursor:pointer; user-select:none; }
  th.sortable:hover { color:var(--cyan); }
  th .arrow { color:var(--cyan); margin-left:4px; }
  .clear { margin-top:10px; }

  /* ---------- charts ---------- */
  .charts { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
  .chart { padding:18px 20px 20px; }
  .chart.wide { grid-column:1 / -1; }
  .chead { display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:14px; }
  .chead h4 { margin:0; font-size:15px; font-weight:700; }
  .csub { color:var(--muted); font-size:12.5px; margin-top:2px; }
  .mini { font:600 11.5px system-ui,sans-serif; color:var(--muted); background:none; border:1px solid var(--line);
          border-radius:8px; padding:4px 10px; cursor:pointer; flex:none; }
  .mini:hover { color:var(--text); border-color:var(--cyan); }
  .nodata { padding:18px 0; }
  .hbars { display:flex; flex-direction:column; gap:4px; }
  .hrow { display:grid; grid-template-columns:minmax(84px,215px) 1fr; align-items:center; gap:12px; padding:5px 6px; border-radius:8px; outline:none; }
  .hrow:hover, .hrow:focus-visible { background:var(--wash); }
  .hrow:focus-visible, .slot:focus-visible { box-shadow:0 0 0 2px var(--cyan); }
  .hlab { font-size:12px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; letter-spacing:.3px; }
  .htrack { display:flex; align-items:center; gap:8px; min-width:0; }
  .hbar { display:block; height:14px; border-radius:0 4px 4px 0; flex:none; transition:filter .15s; }
  .hrow:hover .hbar { filter:brightness(1.2); }
  .hval { font-weight:700; font-size:14px; font-variant-numeric:tabular-nums; }
  .hrow.zero .hval { color:var(--muted); font-weight:500; }
  .tlc { position:relative; padding-left:34px; }
  .tlplot { position:relative; height:150px; border-bottom:1px solid var(--axis); }
  .gl { position:absolute; left:0; right:0; height:1px; background:var(--grid); }
  .ylab { position:absolute; left:-34px; width:28px; text-align:right; font-size:11px; color:var(--muted);
          transform:translateY(-50%); font-variant-numeric:tabular-nums; }
  .tlcols { position:absolute; inset:0; display:flex; }
  .slot { flex:1; min-width:0; display:flex; align-items:flex-end; justify-content:center; outline:none; border-radius:6px 6px 0 0; }
  .slot:hover { background:var(--wash); }
  .tbar { display:block; width:100%; max-width:24px; margin:0 1px; min-height:3px; border-radius:4px 4px 0 0; background:var(--series); transition:filter .15s; }
  .slot:hover .tbar { filter:brightness(1.2); }
  .xlabs { display:flex; justify-content:space-between; margin-top:8px; font-size:11.5px; color:var(--muted); }
  .ctable { max-height:260px; overflow:auto; }
  .tip { position:fixed; z-index:40; pointer-events:none; opacity:0; transition:opacity .12s; max-width:300px;
         background:var(--tip-bg); border:1px solid var(--line); border-radius:10px; padding:8px 12px;
         box-shadow:0 8px 28px var(--shadow); }
  .tip.show { opacity:1; }
  .tiprow { display:flex; align-items:center; gap:8px; font-size:14px; }
  .tipkey { width:14px; height:3px; border-radius:2px; display:inline-block; flex:none; }
  .tiplab { color:var(--muted); font-size:12px; margin-top:2px; }
  @media (max-width:760px) { .charts { grid-template-columns:minmax(0,1fr); } }

  /* ---------- details panel ---------- */
  .case.click, tr.click { cursor:pointer; }
  .case:focus-visible, tr.click:focus-visible { outline:2px solid var(--cyan); outline-offset:2px; }
  .more { margin-top:10px; font-size:12px; color:var(--cyan); letter-spacing:.4px; }
  .scrim { position:fixed; inset:0; z-index:20; background:var(--scrim); backdrop-filter:blur(3px);
           opacity:0; pointer-events:none; transition:opacity .25s; }
  .scrim.open { opacity:1; pointer-events:auto; }
  .panel { position:fixed; top:0; right:0; bottom:0; z-index:21; width:min(480px,100%); overflow-y:auto;
           background:var(--panel-bg); border-left:1px solid var(--line); box-shadow:-20px 0 60px var(--shadow);
           transform:translateX(105%); transition:transform .3s cubic-bezier(.2,.8,.2,1); padding:22px 24px 40px; visibility:hidden; }
  .panel.open { transform:none; visibility:visible; }
  .panel .ph { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:16px; }
  .panel .kicker { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); }
  .panel .title { font:800 22px var(--mono); margin-top:2px; word-break:break-all; }
  .xbtn { font:20px/1 system-ui; width:36px; height:36px; border-radius:10px; cursor:pointer; color:var(--text);
          background:var(--wash); border:1px solid var(--line); flex:none; }
  .xbtn:hover { border-color:var(--pink); color:var(--pink); }
  .panel h3 { margin:24px 0 10px; font-size:12px; letter-spacing:2px; text-transform:uppercase; color:var(--head); }
  .sum { display:flex; align-items:center; gap:18px; padding:16px; border-radius:14px;
         background:color-mix(in srgb,var(--c,var(--NONE)) 8%,transparent); border:1px solid color-mix(in srgb,var(--c,var(--NONE)) 35%,transparent); }
  .sum .big { font-size:13px; color:var(--muted); line-height:1.7; }
  .what { padding:12px 14px; margin-bottom:8px; border-radius:12px; background:var(--what-bg); border:1px solid var(--what-line); }
  .what b { display:block; margin-bottom:2px; color:var(--what-title); }
  .what span { color:var(--muted); font-size:13.5px; }
  ul.tl { list-style:none; margin:0 0 0 6px; padding:0 0 0 18px; border-left:2px solid var(--line); }
  ul.tl li { position:relative; padding:0 0 14px; font-size:13.5px; }
  ul.tl li::before { content:""; position:absolute; left:-25px; top:5px; width:10px; height:10px; border-radius:50%;
                     background:var(--cyan); box-shadow:0 0 10px var(--cyan); }
  ul.tl .t { color:var(--muted); font-size:12px; display:block; }
  ul.todo { margin:0; padding-left:20px; color:var(--todo-text); font-size:14px; }
  ul.todo li { margin-bottom:6px; }
  .warn { padding:11px 14px; border-radius:12px; font-size:13px; margin:10px 0; color:var(--warn-text);
          background:color-mix(in srgb,var(--MEDIUM) 10%,transparent); border:1px solid color-mix(in srgb,var(--MEDIUM) 40%,transparent); }
  .cmd { font:12.5px/1.5 var(--mono); padding:12px 14px; border-radius:10px; background:var(--cmd-bg); border:1px solid var(--line);
         color:var(--cmd-text); word-break:break-all; user-select:all; margin:8px 0; }
  .row { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
  .fine { color:var(--muted); font-size:12px; margin-top:18px; }
  .toast { position:fixed; left:50%; bottom:28px; z-index:30; transform:translate(-50%,20px); opacity:0; pointer-events:none;
           background:var(--toast-bg); border:1px solid var(--cyan); color:var(--text); padding:10px 18px; border-radius:12px;
           font-size:14px; box-shadow:0 0 24px rgba(34,211,238,.3); transition:.25s; }
  .toast.show { opacity:1; transform:translate(-50%,0); }

  /* ---------- alert table ---------- */
  .wrap { overflow-x:auto; }
  table { width:100%; border-collapse:collapse; }
  th,td { text-align:left; padding:12px 16px; font-size:14px; border-bottom:1px solid var(--rowline); white-space:nowrap; }
  th { color:var(--muted); font-size:11.5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; }
  tbody tr:hover td { background:rgba(34,211,238,.05); }
  td.mono { font-family:var(--mono); }
  .cases > .empty { grid-column:1 / -1; }
  .empty { padding:30px; text-align:center; color:var(--muted); }
  .empty b { display:block; font-size:28px; margin-bottom:6px; }

  footer { text-align:center; color:var(--muted); font-size:12px; padding:10px 0 30px; letter-spacing:.4px; }

  @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.35; } }
  @media (max-width:640px) { .top, main { padding-left:16px; padding-right:16px; } .threat { flex-wrap:wrap; } .threat .why { margin-left:0; text-align:left; } }
  @media (prefers-reduced-motion:reduce) { * { animation:none !important; transition:none !important; } }
  .select { font:600 13px system-ui,sans-serif; color:var(--text); background:var(--btn-bg); border:1px solid var(--line);
            border-radius:10px; padding:8px 10px; cursor:pointer; }
  .select:hover { border-color:var(--cyan); }
  .select:disabled { opacity:.55; cursor:default; }
  .select option { background:var(--bg); color:var(--text); }
  .panel .title.plain { font:800 20px system-ui,sans-serif; }
  .kbd { font:11px var(--mono); border:1px solid var(--line); border-radius:5px; padding:1px 6px; background:var(--wash); }
  :root[data-theme="light"] .bg {
    background:
      radial-gradient(900px 500px at 12% -10%, rgba(14,116,144,.10), transparent 60%),
      radial-gradient(800px 500px at 100% 0%, rgba(109,40,217,.10), transparent 60%),
      linear-gradient(rgba(30,50,100,.05) 1px, transparent 1px) 0 0/44px 44px,
      linear-gradient(90deg, rgba(30,50,100,.05) 1px, transparent 1px) 0 0/44px 44px;
  }
</style></head>
<body>
<div class="bg"></div>

<header class="top">
  <div class="brand">
    <svg width="38" height="38" viewBox="0 0 40 40" fill="none">
      <defs><linearGradient id="g" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
      <path d="M20 3 34 8v11c0 9-6 15-14 18C12 34 6 28 6 19V8z" stroke="url(#g)" stroke-width="2.2" fill="rgba(34,211,238,.08)"/>
      <circle cx="20" cy="20" r="6" stroke="url(#g)" stroke-width="2"/><circle cx="20" cy="20" r="1.8" fill="#22d3ee"/>
    </svg>
    <div><h1>LogSentinel</h1><div class="sub">Security log analyzer</div></div>
  </div>
  <div class="top-actions">
    <span class="pill" id="live"><i></i><span id="livetext">LIVE</span></span>
    <span class="muted" id="updated">Loading...</span>
    <div class="btns" id="actions"></div>
  </div>
</header>

<main>
  <section class="glass threat" id="threat"></section>
  <div id="hints"></div>
  <section class="kpis" id="stats"></section>

  <nav class="tabs" id="tabs"></nav>
  <div class="glass toolbar" id="toolbar">
    <input id="q" type="search" placeholder="Search IP address, user or rule...   (press /)" autocomplete="off">
    <div class="filters" id="filters"></div>
    <span class="muted" id="count"></span>
  </div>
  <div id="view"></div>
</main>
<div class="scrim" id="scrim"></div>
<aside class="panel" id="panel" role="dialog" aria-modal="true" aria-label="Details" aria-hidden="true"></aside>
<div class="toast" id="toast" role="status"></div>
<footer>Runs only on this PC &middot; your logs never leave your computer</footer>

<script>
const token = new URLSearchParams(location.search).get("token") || "";
const NS = "http://www.w3.org/2000/svg";
const ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];

function el(tag, text, cls) {
  const e = document.createElement(tag);
  if (text !== undefined && text !== null) e.textContent = String(text);
  if (cls) e.className = cls;
  return e;
}

const SEEN_RINGS = new Set();
const LAST_KPI = {};

function ringSvg(score, key) {
  const s = document.createElementNS(NS, "svg");
  s.setAttribute("viewBox", "0 0 72 72");
  const r = 29, full = 2 * Math.PI * r;
  const mk = (cls) => {
    const c = document.createElementNS(NS, "circle");
    c.setAttribute("cx", 36); c.setAttribute("cy", 36); c.setAttribute("r", r);
    c.setAttribute("fill", "none"); c.setAttribute("stroke-width", 6); c.setAttribute("stroke-linecap", "round");
    c.setAttribute("class", cls); return c;
  };
  s.appendChild(mk("track"));
  const bar = mk("bar");
  const target = (Math.max(0, Math.min(100, score)) / 100 * full) + " " + full;
  s.appendChild(bar);
  if (SEEN_RINGS.has(key)) {
    bar.style.transition = "none";            // already shown before: no replay
    bar.setAttribute("stroke-dasharray", target);
  } else {
    SEEN_RINGS.add(key);
    bar.setAttribute("stroke-dasharray", "0 " + full);
    requestAnimationFrame(() => requestAnimationFrame(() => bar.setAttribute("stroke-dasharray", target)));
  }
  return s;
}

function countUp(node, to, from) {
  to = Number(to) || 0;
  const start = Number(from || 0);
  if (start === to) { node.textContent = to; return; }
  const t0 = performance.now();
  (function tick(t) {
    const k = Math.min(1, (t - t0) / 600);
    node.textContent = Math.round(start + (to - start) * k);
    if (k < 1) requestAnimationFrame(tick);
  })(t0);
}

function kpi(label, value) {
  const c = el("div", null, "glass kpi");
  const n = el("div", 0, "num");
  c.appendChild(n); c.appendChild(el("div", label, "lab"));
  const before = LAST_KPI[label];
  LAST_KPI[label] = value;
  countUp(n, value, before === undefined ? 0 : before);
  return c;
}

function hints(d) {
  const out = [], i = d.info || {}, s = d.scan || {};
  if (d.demo) out.push({t: "DEMO MODE: everything here is made up (sample IP addresses). Nothing was read from your PC.", demo: true});
  if (s.status === "error") out.push({t: "The last scan failed: " + s.message});
  if (i.live && i.admin === false) out.push({t: "This window is not running as Administrator, so Windows may be hiding the Security log from LogSentinel. Close it, run: logsentry start, and accept the permission prompt."});
  if (i.live && i.failures === 0) out.push({t: 'No failed logins were found in the last ' + i.hours + ' hours. That is either good news, or Windows is not recording failed logins. To check, open PowerShell as Administrator and run: auditpol /get /subcategory:"Logon" (it should list Failure).'});
  else if (i.live && i.alerts === 0) out.push({t: i.failures + " failed logins were found, but not enough to trigger a rule (for example 5 failures within one minute). A few typos are normal."});
  if (i.live) out.push({t: "What is counted: failed logins on this PC and from other computers. Successful logins are only counted when they come from another computer."});
  return out;
}

function threatBanner(d) {
  const box = document.getElementById("threat");
  let level = "ALL CLEAR", why = "No incidents. Nothing suspicious was found.", cls = "";
  for (const sev of ORDER) {
    const n = d.incidents.filter(x => x.severity === sev).length;
    if (n) { level = sev; why = n + " " + sev.toLowerCase() + " incident" + (n > 1 ? "s need" : " needs") + " attention."; cls = "sev-" + sev; break; }
  }
  box.className = "glass threat " + cls;
  box.replaceChildren(el("span", null, "dot"));
  const mid = el("div");
  mid.appendChild(el("div", "Current threat level", "label"));
  mid.appendChild(el("div", level, "level"));
  box.appendChild(mid);
  box.appendChild(el("div", why, "why"));
}

function incidentCard(x) {
  const card = el("div", null, "glass case sev-" + x.severity);
  const ring = el("div", null, "ring");
  ring.appendChild(ringSvg(Number(x.risk_score) || 0, x.ip));
  ring.appendChild(el("b", x.risk_score));
  card.appendChild(ring);

  const body = el("div");
  const head = el("div");
  head.appendChild(el("span", x.ip, "ip"));
  const copy = el("button", "copy", "copy");
  copy.onclick = async (ev) => {
    ev.stopPropagation();
    toast((await copyText(String(x.ip))) ? "Copied " + x.ip : "Could not copy. Select it by hand.");
  };
  head.appendChild(copy);
  body.appendChild(head);

  const line = el("div", null, "meta");
  line.appendChild(el("span", x.severity, "tag"));
  line.appendChild(document.createTextNode("  " + (x.status || "")));
  body.appendChild(line);
  body.appendChild(el("div", "First seen " + x.first_seen, "meta"));
  body.appendChild(el("div", "Last seen  " + x.last_seen, "meta"));
  const chips = el("div", null, "chips");
  (x.rules || []).forEach(r => chips.appendChild(el("span", r, "chip")));
  body.appendChild(chips);
  body.appendChild(el("div", "View details →", "more"));
  card.appendChild(body);
  card.classList.add("click");
  card.tabIndex = 0;
  card.setAttribute("role", "button");
  card.onclick = () => openPanel({ip: x.ip});
  card.onkeydown = (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openPanel({ip: x.ip}); } };
  return card;
}

const RULES = {
  BRUTE_FORCE: {
    title: "Password guessing (brute force)",
    what: "One address got many passwords wrong in a short time. That usually means a program is guessing passwords.",
    todo: ["Block the address (see below).", "Make sure the accounts being attacked have long, unique passwords.", "Turn on account lockout in Windows if you can."],
  },
  USERNAME_ENUMERATION: {
    title: "Hunting for usernames",
    what: "One address tried many different usernames. Attackers do this to find out which accounts exist.",
    todo: ["Block the address (see below).", "Rename or disable default accounts such as Administrator or Guest if you do not use them."],
  },
  SUCCESS_AFTER_FAILURE: {
    title: "Possible break-in",
    what: "A login worked right after many failures from the same address. The password may have been guessed.",
    todo: ["Change the password of that account now, from a device you trust.", "Sign out all sessions of that account.", "Look at what the account did after the login (new accounts, new files, new programs).", "Block the address (see below)."],
  },
  PASSWORD_SPRAY: {
    title: "Password spraying",
    what: "Many different addresses tried to log in to the same account. This is a slower, spread-out way of guessing passwords that avoids simple blocking.",
    todo: ["Change the password of the targeted account to a long, unique one.", "Turn on two-step verification where you can.", "Block the addresses involved."],
  },
  ANOMALY: {
    title: "Unusual spike",
    what: "There were far more failed logins than normal during one period.",
    todo: ["Look at which addresses and accounts were involved in that period (Alerts tab).", "If it was not you or your family, treat it like password guessing."],
  },
};

function ruleInfo(name) {
  return RULES[name] || {title: name, what: "This rule flagged unusual login activity.", todo: ["Check the Windows Security log around these times."]};
}

const IP4 = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/;
const IP6 = /^[0-9a-fA-F:.]{2,45}$/;

function validIp(ip) {
  const v = String(ip || "");
  return IP4.test(v) || (IP6.test(v) && (v.match(/:/g) || []).length >= 2);
}

function isPrivateIp(ip) {
  const m = String(ip).match(/^(\d+)\.(\d+)\./);
  if (!m) return false;
  const a = +m[1], b = +m[2];
  return a === 10 || a === 127 || (a === 192 && b === 168) || (a === 172 && b >= 16 && b <= 31) || (a === 169 && b === 254);
}

function blockCmd(ip) {
  return 'New-NetFirewallRule -DisplayName "LogSentinel block ' + ip + '" -Direction Inbound -Action Block -RemoteAddress ' + ip;
}
function undoCmd(ip) {
  return 'Remove-NetFirewallRule -DisplayName "LogSentinel block ' + ip + '"';
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
  try {
    const t = document.createElement("textarea");
    t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
    document.body.appendChild(t); t.select();
    const ok = document.execCommand("copy");
    t.remove(); return ok;
  } catch (e) { return false; }
}

let toastTimer = null;
function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg; t.className = "toast show";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.className = "toast", 2200);
}

let lastFocus = null;
function panelOpen() { return document.getElementById("panel").classList.contains("open"); }

function closePanel() {
  document.getElementById("panel").classList.remove("open");
  document.getElementById("panel").setAttribute("aria-hidden", "true");
  document.getElementById("scrim").classList.remove("open");
  if (lastFocus && lastFocus.focus) lastFocus.focus();
}

function section(title) { return el("h3", title); }

function copyButton(label, text, doneMsg) {
  const b = el("button", label, "btn");
  b.onclick = async () => toast((await copyText(text)) ? doneMsg : "Could not copy. Select the text by hand.");
  return b;
}

function openPanel(spec) {
  const d = DATA;
  if (!d) return;
  const ip = spec.ip || null;
  const inc = ip ? d.incidents.find(x => x.ip === ip) : null;
  let related = ip ? d.alerts.filter(a => a.ip === ip) : (spec.alert ? [spec.alert] : []);
  related = related.slice().sort((a, b) => String(a.last_seen).localeCompare(String(b.last_seen)));
  const subject = ip || (spec.alert && (spec.alert.username || spec.alert.rule)) || "-";

  const box = document.getElementById("panel");
  const parts = [];

  // header
  const head = el("div", null, "ph");
  const left = el("div");
  left.appendChild(el("div", inc ? "Incident" : "Alert", "kicker"));
  left.appendChild(el("div", subject, "title"));
  head.appendChild(left);
  const x = el("button", "×", "xbtn");
  x.setAttribute("aria-label", "Close details");
  x.onclick = closePanel;
  head.appendChild(x);
  parts.push(head);

  // summary
  if (inc) {
    const sum = el("div", null, "sum sev-" + inc.severity);
    const ring = el("div", null, "ring");
    ring.appendChild(ringSvg(Number(inc.risk_score) || 0, "panel-" + Date.now()));
    ring.appendChild(el("b", inc.risk_score));
    sum.appendChild(ring);
    const info = el("div", null, "big");
    const tagLine = el("div");
    tagLine.appendChild(el("span", inc.severity, "tag"));
    tagLine.appendChild(document.createTextNode("  " + (inc.status || "")));
    info.appendChild(tagLine);
    info.appendChild(el("div", "First seen " + inc.first_seen));
    info.appendChild(el("div", "Last seen " + inc.last_seen));
    sum.appendChild(info);
    parts.push(sum);
  } else if (spec.alert) {
    const info = el("div", null, "big");
    info.appendChild(el("div", "Last seen " + spec.alert.last_seen));
    info.appendChild(el("div", "Happened " + (spec.alert.occurrences ?? 1) + " time(s)"));
    parts.push(info);
  }

  // what happened
  const ruleNames = Array.from(new Set(inc && inc.rules && inc.rules.length ? inc.rules : related.map(a => a.rule)));
  parts.push(section("What happened"));
  if (!ruleNames.length) parts.push(el("div", "No details are stored for this item.", "muted"));
  ruleNames.forEach(name => {
    const info = ruleInfo(name), w = el("div", null, "what");
    w.appendChild(el("b", info.title + "  (" + name + ")"));
    w.appendChild(el("span", info.what));
    parts.push(w);
  });

  // timeline
  if (related.length) {
    parts.push(section("Timeline"));
    const ul = el("ul", null, "tl");
    related.forEach(a => {
      const li = el("li");
      li.appendChild(el("span", a.last_seen, "t"));
      li.appendChild(document.createTextNode(a.rule + (a.username ? " (account: " + a.username + ")" : "") + "  x" + (a.occurrences ?? 1)));
      ul.appendChild(li);
    });
    parts.push(ul);
  }

  // what to do
  const todo = [];
  ruleNames.forEach(n => ruleInfo(n).todo.forEach(t => { if (!todo.includes(t)) todo.push(t); }));
  if (todo.length) {
    parts.push(section("What to do now"));
    const ul = el("ul", null, "todo");
    todo.forEach(t => ul.appendChild(el("li", t)));
    parts.push(ul);
  }

  // block this IP
  if (ip && validIp(ip)) {
    parts.push(section("Block this address"));
    if (isPrivateIp(ip)) {
      parts.push(el("div", "This address is inside a private network. It may be your router or another device of yours. Make sure you really want to block it, or you could lock yourself out.", "warn"));
    }
    parts.push(el("div", "1. Open PowerShell as Administrator.   2. Paste this command.   3. Press Enter.", "muted"));
    parts.push(el("div", blockCmd(ip), "cmd"));
    const row = el("div", null, "row");
    row.appendChild(copyButton("Copy block command", blockCmd(ip), "Block command copied"));
    row.appendChild(copyButton("Copy undo command", undoCmd(ip), "Undo command copied"));
    row.appendChild(copyButton("Copy address", ip, "Copied " + ip));
    parts.push(row);
    parts.push(el("div", "This blocks new connections from that address to this PC. LogSentinel never changes your firewall by itself. It only copies the command, and you decide whether to run it.", "fine"));
  } else if (ip === "LOCAL") {
    parts.push(section("About LOCAL"));
    parts.push(el("div", "LOCAL means the failed logins were made on this PC itself (the sign-in screen, the lock screen, or this PC connecting to itself). There is nothing to block. If it was not you, check who can sit at this PC or reach it by Remote Desktop.", "warn"));
  }

  box.replaceChildren(...parts);
  lastFocus = document.activeElement;
  box.classList.add("open");
  box.setAttribute("aria-hidden", "false");
  box.scrollTop = 0;
  document.getElementById("scrim").classList.add("open");
  x.focus();
}

document.getElementById("scrim").addEventListener("click", closePanel);

// ---------- charts ----------
const SEV_CHART = {CRITICAL: "var(--sevc-CRITICAL)", HIGH: "var(--sevc-HIGH)", MEDIUM: "var(--sevc-MEDIUM)", LOW: "var(--sevc-LOW)"};
const SERIES = "var(--series)";
const CHART_TABLE = {};

const tip = document.createElement("div");
tip.className = "tip";
document.body.appendChild(tip);

function showTip(x, y, color, value, label) {
  tip.replaceChildren();
  const row = el("div", null, "tiprow");
  const key = el("i", null, "tipkey");
  key.style.background = color;
  row.appendChild(key);
  row.appendChild(el("b", value));
  tip.appendChild(row);
  tip.appendChild(el("div", label, "tiplab"));
  tip.className = "tip show";
  const w = tip.offsetWidth, h = tip.offsetHeight;
  let left = x + 14, top = y - h - 12;
  if (left + w > window.innerWidth - 8) left = x - w - 14;
  if (top < 8) top = y + 18;
  tip.style.left = Math.max(8, left) + "px";
  tip.style.top = top + "px";
}
function hideTip() { tip.className = "tip"; }

function attachTip(node, color, value, label) {
  node.tabIndex = 0;
  node.addEventListener("pointermove", (ev) => showTip(ev.clientX, ev.clientY, color, value, label));
  node.addEventListener("pointerleave", hideTip);
  node.addEventListener("focus", () => {
    const r = node.getBoundingClientRect();
    showTip(r.left + r.width / 2, r.top, color, value, label);
  });
  node.addEventListener("blur", hideTip);
}

function plural(n, noun) { return n + " " + noun + (n === 1 ? "" : "s"); }

function hbars(items, noun) {
  const max = Math.max(1, ...items.map(i => i.value));
  const box = el("div", null, "hbars");
  items.forEach(i => {
    const row = el("div", null, "hrow" + (i.value === 0 ? " zero" : ""));
    const lab = el("div", i.label, "hlab");
    lab.title = i.label;
    const track = el("div", null, "htrack");
    const bar = el("span", null, "hbar");
    bar.style.background = i.color;
    bar.style.width = "calc((100% - 46px) * " + (i.value / max) + ")";
    track.appendChild(bar);
    track.appendChild(el("span", i.value, "hval"));
    row.appendChild(lab);
    row.appendChild(track);
    attachTip(row, i.color, plural(i.value, noun), i.label);
    box.appendChild(row);
  });
  return box;
}

function simpleTable(headers, rows) {
  const t = el("table"), hr = el("tr");
  headers.forEach(h => hr.appendChild(el("th", h)));
  const thead = el("thead"); thead.appendChild(hr); t.appendChild(thead);
  const tb = el("tbody");
  rows.forEach(r => {
    const tr = el("tr");
    r.forEach(c => tr.appendChild(el("td", c)));
    tb.appendChild(tr);
  });
  t.appendChild(tb);
  const box = el("div", null, "ctable");
  box.appendChild(t);
  return box;
}

function parseTime(v) {
  const m = String(v).match(/^(\d{4})-(\d\d)-(\d\d)[ T](\d\d):(\d\d)(?::(\d\d))?/);
  if (!m) return null;
  return new Date(+m[1], m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0)).getTime();
}

const STEPS = [1, 2, 5, 10, 15, 30, 60, 120, 180, 360, 720, 1440].map(m => m * 60000);
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
function pad2(n) { return String(n).padStart(2, "0"); }

function timelineData(alerts) {
  const times = alerts.map(a => parseTime(a.last_seen)).filter(t => t !== null);
  if (!times.length) return null;
  const min = Math.min(...times), max = Math.max(...times);
  let step = STEPS[STEPS.length - 1];
  for (const s of STEPS) { if (Math.floor((max - min) / s) + 1 <= 24) { step = s; break; } }
  const off = new Date(min).getTimezoneOffset() * 60000;     // keep buckets on local clock boundaries
  const start = Math.floor((min - off) / step) * step + off;
  const count = Math.floor((max - start) / step) + 1;
  const buckets = [];
  for (let i = 0; i < count; i++) buckets.push({t: start + i * step, n: 0});
  times.forEach(t => { buckets[Math.floor((t - start) / step)].n++; });
  const multiDay = (max - min) > 24 * 3600000;
  const fmt = (t) => {
    const d = new Date(t);
    if (step >= 1440 * 60000) return MONTHS[d.getMonth()] + " " + d.getDate();
    const hm = pad2(d.getHours()) + ":" + pad2(d.getMinutes());
    return multiDay ? MONTHS[d.getMonth()] + " " + d.getDate() + " " + hm : hm;
  };
  return {buckets, step, fmt};
}

function niceTop(max) {
  if (max <= 5) return Math.max(1, max);
  const unit = Math.pow(10, Math.floor(Math.log10(max)));
  return Math.ceil(max / unit) * unit;
}

function timelineChart(alerts) {
  const td = timelineData(alerts);
  if (!td) return el("div", "No timestamps to chart.", "muted nodata");
  const top = niceTop(Math.max(...td.buckets.map(b => b.n)));
  const wrap = el("div", null, "tlc");
  const plot = el("div", null, "tlplot");

  const ticks = [[0, top]];
  if (top % 2 === 0 && top >= 2) ticks.push([50, top / 2]);
  ticks.push([100, 0]);
  ticks.forEach(([pct, label]) => {
    if (pct < 100) { const g = el("div", null, "gl"); g.style.top = pct + "%"; plot.appendChild(g); }
    const y = el("span", label, "ylab");
    y.style.top = pct + "%";
    plot.appendChild(y);
  });

  const cols = el("div", null, "tlcols");
  td.buckets.forEach(b => {
    const slot = el("div", null, "slot");
    if (b.n > 0) {
      const bar = el("span", null, "tbar");
      bar.style.height = (b.n / top * 100) + "%";
      slot.appendChild(bar);
    }
    attachTip(slot, SERIES, plural(b.n, "alert"), td.fmt(b.t) + (td.step >= 60000 * 1440 ? "" : " - " + td.fmt(b.t + td.step)));
    cols.appendChild(slot);
  });
  plot.appendChild(cols);
  wrap.appendChild(plot);

  const xl = el("div", null, "xlabs");
  const n = td.buckets.length;
  xl.appendChild(el("span", td.fmt(td.buckets[0].t)));
  if (n >= 3) xl.appendChild(el("span", td.fmt(td.buckets[Math.floor(n / 2)].t)));
  if (n >= 2) xl.appendChild(el("span", td.fmt(td.buckets[n - 1].t)));
  wrap.appendChild(xl);
  return wrap;
}

function chartCard(id, title, sub, summary, buildChart, buildTable, wide) {
  const card = el("div", null, "glass chart" + (wide ? " wide" : ""));
  const head = el("div", null, "chead");
  const t = el("div");
  t.appendChild(el("h4", title));
  t.appendChild(el("div", sub, "csub"));
  head.appendChild(t);
  const btn = el("button", CHART_TABLE[id] ? "Chart" : "Table", "mini");
  btn.setAttribute("aria-pressed", CHART_TABLE[id] ? "true" : "false");
  btn.title = CHART_TABLE[id] ? "Show the chart" : "Show the numbers as a table";
  btn.onclick = () => { CHART_TABLE[id] = !CHART_TABLE[id]; renderView(); };
  head.appendChild(btn);
  card.appendChild(head);
  const body = el("div", null, "cbody");
  body.setAttribute("role", "group");
  body.setAttribute("aria-label", title + ". " + summary);
  body.appendChild(CHART_TABLE[id] ? buildTable() : buildChart());
  card.appendChild(body);
  return card;
}

function chartsGrid(d) {
  const grid = el("section", null, "charts");

  const sev = ORDER.map(s => ({label: s, value: d.incidents.filter(x => x.severity === s).length, color: SEV_CHART[s]}));
  grid.appendChild(chartCard("sev", "Incidents by severity", "how serious each case is",
    sev.map(i => i.label + " " + i.value).join(", "),
    () => d.incidents.length ? hbars(sev, "incident") : el("div", "No incidents to chart.", "muted nodata"),
    () => simpleTable(["Severity", "Incidents"], sev.map(i => [i.label, i.value]))));

  const byRule = {};
  d.alerts.forEach(a => { byRule[a.rule] = (byRule[a.rule] || 0) + (Number(a.occurrences) || 1); });
  const rules = Object.entries(byRule).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({label: k, value: v, color: SERIES}));
  grid.appendChild(chartCard("rules", "Which rules fired most", "total times each rule triggered",
    rules.map(i => i.label + " " + i.value).join(", "),
    () => rules.length ? hbars(rules, "time") : el("div", "No alerts to chart.", "muted nodata"),
    () => simpleTable(["Rule", "Times fired"], rules.map(i => [i.label, i.value]))));

  const td = timelineData(d.alerts);
  grid.appendChild(chartCard("time", "When alerts were last seen", "number of alerts per time slot",
    td ? td.buckets.length + " time slots, " + d.alerts.length + " alerts in total" : "no data",
    () => d.alerts.length ? timelineChart(d.alerts) : el("div", "No alerts to chart.", "muted nodata"),
    () => simpleTable(["Time slot", "Alerts"], td ? td.buckets.map(b => [td.fmt(b.t), b.n]) : []),
    true));
  return grid;
}

function helpBlock(title, text) {
  const w = el("div", null, "what");
  w.appendChild(el("b", title));
  w.appendChild(el("span", text));
  return w;
}

function openHelp() {
  const box = document.getElementById("panel");
  const parts = [];
  const head = el("div", null, "ph");
  const left = el("div");
  left.appendChild(el("div", "Help", "kicker"));
  left.appendChild(el("div", "How to read this page", "title plain"));
  head.appendChild(left);
  const x = el("button", "×", "xbtn");
  x.setAttribute("aria-label", "Close help");
  x.onclick = closePanel;
  head.appendChild(x);
  parts.push(head);

  parts.push(section("The basics"));
  parts.push(helpBlock("Alert", "One rule noticed something odd, for example 'too many wrong passwords from one address'."));
  parts.push(helpBlock("Incident", "All the alerts for one address, bundled into one case with a risk score from 0 to 100. Higher means more serious. Click a case to see its story."));
  parts.push(helpBlock("Threat level (the big banner)", "The most serious incident right now. ALL CLEAR means nothing suspicious was found in the time range you scanned."));
  parts.push(helpBlock("Severity colours", "Red = critical, orange = high, yellow = medium, green = low. The colour always comes with a word, so you never have to rely on colour alone."));
  parts.push(helpBlock("LOCAL", "Failed logins made on this PC itself (sign-in screen, lock screen). It is not an outside address, so there is nothing to block."));

  parts.push(section("The rules"));
  Object.keys(RULES).forEach(name => parts.push(helpBlock(RULES[name].title + "  (" + name + ")", RULES[name].what)));

  parts.push(section("Buttons and shortcuts"));
  parts.push(helpBlock("Time range + Rescan now", "Choose how far back to look (1 hour to 7 days). Changing it scans again straight away."));
  parts.push(helpBlock("Pause", "Stops the page from refreshing by itself while you read."));
  parts.push(helpBlock("Download", "Saves the alerts as CSV (Excel), HTML (a page you can print) or JSON (for other programs)."));
  parts.push(helpBlock("Charts: Table button", "Shows the same numbers as a plain table, for screen readers or copying."));
  const keys = el("div", null, "what");
  keys.appendChild(el("b", "Keyboard"));
  const k = el("span");
  [["/", " search   "], ["Esc", " close or clear   "], ["?", " this help   "], ["Tab", " move around, Enter opens a row"]].forEach(([key, text]) => {
    k.appendChild(el("span", key, "kbd")); k.appendChild(document.createTextNode(text));
  });
  keys.appendChild(k);
  parts.push(keys);

  parts.push(section("Your data"));
  parts.push(helpBlock("Stays on this PC", "This page is served only to this computer and only works with the secret link shown in the LogSentinel window. Nothing is uploaded anywhere, and LogSentinel never changes your firewall by itself."));

  box.replaceChildren(...parts);
  lastFocus = document.activeElement;
  box.classList.add("open");
  box.setAttribute("aria-hidden", "false");
  box.scrollTop = 0;
  document.getElementById("scrim").classList.add("open");
  x.focus();
}

const ui = {tab: "overview", q: "", filter: "ALL", sortKey: "last_seen", sortDir: -1, paused: false};
let DATA = null;

function emptyBox(title, text, cls) {
  const e = el("div", null, (cls || "glass") + " empty");
  e.appendChild(el("b", title));
  e.appendChild(document.createTextNode(text));
  return e;
}

function noMatch() {
  const e = emptyBox("∅", "Nothing matches your search or filter.");
  const b = el("button", "Clear search and filter", "btn clear");
  b.onclick = () => { ui.q = ""; ui.filter = "ALL"; document.getElementById("q").value = ""; renderView(); };
  e.appendChild(el("div")); e.lastChild.appendChild(b);
  return e;
}

function heading(title, sub) {
  const h = el("h2", title + " ");
  if (sub) h.appendChild(el("small", sub));
  return h;
}

function whoOf(a) { return a.ip || a.username || "-"; }

function alertTable(rows, sortable) {
  const t = el("table"), thead = el("thead"), hr = el("tr");
  [["last_seen", "Last seen"], ["rule", "Rule"], ["who", "Who"], ["occurrences", "Times"]].forEach(([key, label]) => {
    const th = el("th", label);
    if (sortable) {
      th.className = "sortable";
      if (ui.sortKey === key) th.appendChild(el("span", ui.sortDir > 0 ? "▲" : "▼", "arrow"));
      th.onclick = () => {
        if (ui.sortKey === key) ui.sortDir = -ui.sortDir; else { ui.sortKey = key; ui.sortDir = 1; }
        renderView();
      };
    }
    hr.appendChild(th);
  });
  thead.appendChild(hr); t.appendChild(thead);
  const tb = el("tbody");
  rows.forEach(a => {
    const tr = el("tr", null, "click");
    tr.tabIndex = 0;
    tr.title = "Click for details";
    tr.onclick = () => openPanel({ip: a.ip || null, alert: a});
    tr.onkeydown = (ev) => { if (ev.key === "Enter") { ev.preventDefault(); openPanel({ip: a.ip || null, alert: a}); } };
    tr.appendChild(el("td", a.last_seen));
    const tdRule = el("td"); tdRule.appendChild(el("span", a.rule, "chip")); tr.appendChild(tdRule);
    tr.appendChild(el("td", whoOf(a), "mono"));
    tr.appendChild(el("td", "x" + (a.occurrences ?? 1)));
    tb.appendChild(tr);
  });
  t.appendChild(tb);
  const wrap = el("div", null, "glass wrap");
  wrap.appendChild(t);
  return wrap;
}

function matches(parts) {
  const q = ui.q.trim().toLowerCase();
  if (!q) return true;
  return parts.some(p => String(p === null || p === undefined ? "" : p).toLowerCase().includes(q));
}

function sortRows(rows) {
  const val = (a) => ui.sortKey === "who" ? whoOf(a) : a[ui.sortKey];
  return rows.slice().sort((x, y) => {
    const a = val(x), b = val(y);
    if (typeof a === "number" && typeof b === "number") return (a - b) * ui.sortDir;
    return String(a ?? "").localeCompare(String(b ?? "")) * ui.sortDir;
  });
}

function setFilters(options) {
  const box = document.getElementById("filters");
  box.replaceChildren(...options.map(o => {
    const b = el("button", o.label, "fchip" + (o.cls ? " " + o.cls : "") + (ui.filter === o.value ? " on" : ""));
    b.onclick = () => { ui.filter = o.value; renderView(); };
    return b;
  }));
}

function renderTabs() {
  const d = DATA;
  const tabs = [["overview", "Overview", null], ["incidents", "Incidents", d.incidents.length], ["alerts", "Alerts", d.alerts.length]];
  document.getElementById("tabs").replaceChildren(...tabs.map(([key, label, n]) => {
    const b = el("button", label, "tab" + (ui.tab === key ? " on" : ""));
    if (n !== null) b.appendChild(el("em", n));
    b.onclick = () => setTab(key);
    return b;
  }));
}

function setTab(key) {
  if (ui.tab !== key) { ui.tab = key; ui.filter = "ALL"; }
  try { history.replaceState(null, "", location.pathname + location.search + "#" + key); } catch (e) {}
  renderView();
}

function renderView() {
  if (!DATA) return;
  const d = DATA, view = document.getElementById("view");
  document.getElementById("toolbar").style.display = ui.tab === "overview" ? "none" : "";
  hideTip();
  renderTabs();

  if (ui.tab === "overview") {
    const parts = [heading("Top incidents", "highest risk first")];
    const top = d.incidents.slice().sort((a, b) => b.risk_score - a.risk_score).slice(0, 3);
    const grid = el("section", null, "cases");
    if (top.length) top.forEach(x => grid.appendChild(incidentCard(x)));
    else grid.appendChild(emptyBox("✓", "No incidents yet. Nothing suspicious was found."));
    parts.push(grid);
    if (d.incidents.length > 3) {
      const more = el("button", "See all " + d.incidents.length + " incidents", "btn clear");
      more.onclick = () => setTab("incidents");
      parts.push(more);
    }
    parts.push(heading("Insights", "what the numbers look like"));
    parts.push(chartsGrid(d));
    parts.push(heading("Latest alerts", "newest first"));
    const latest = d.alerts.slice().sort((a, b) => String(b.last_seen).localeCompare(String(a.last_seen))).slice(0, 6);
    parts.push(latest.length ? alertTable(latest, false) : emptyBox("✓", "No alerts stored yet."));
    view.replaceChildren(...parts);
    return;
  }

  if (ui.tab === "incidents") {
    const opts = [{value: "ALL", label: "All (" + d.incidents.length + ")"}].concat(ORDER.map(s => ({
      value: s, cls: "sev-" + s, label: s + " (" + d.incidents.filter(x => x.severity === s).length + ")",
    })));
    setFilters(opts);
    const rows = d.incidents
      .filter(x => ui.filter === "ALL" || x.severity === ui.filter)
      .filter(x => matches([x.ip, x.severity, x.status, (x.rules || []).join(" ")]))
      .sort((a, b) => b.risk_score - a.risk_score);
    document.getElementById("count").textContent = "Showing " + rows.length + " of " + d.incidents.length;
    const grid = el("section", null, "cases");
    if (rows.length) rows.forEach(x => grid.appendChild(incidentCard(x)));
    else grid.appendChild(d.incidents.length ? noMatch() : emptyBox("✓", "No incidents yet. Nothing suspicious was found."));
    view.replaceChildren(grid);
    return;
  }

  // alerts tab
  const rules = Array.from(new Set(d.alerts.map(a => a.rule))).sort();
  setFilters([{value: "ALL", label: "All rules"}].concat(rules.map(r => ({value: r, label: r}))));
  const rows = sortRows(d.alerts
    .filter(a => ui.filter === "ALL" || a.rule === ui.filter)
    .filter(a => matches([a.rule, a.ip, a.username, a.last_seen])));
  document.getElementById("count").textContent = "Showing " + rows.length + " of " + d.alerts.length;
  if (rows.length) view.replaceChildren(alertTable(rows, true));
  else view.replaceChildren(d.alerts.length ? noMatch() : emptyBox("✓", "No alerts stored yet."));
}

function render(d) {
  DATA = d;
  const i = d.info || {}, s = d.scan || {};
  threatBanner(d);

  document.getElementById("hints").replaceChildren(
    ...hints(d).map(h => el("div", h.t, "glass note" + (h.demo ? " demo" : ""))));

  const cards = [
    kpi("Alerts", d.alerts.length),
    kpi("Incidents", d.incidents.length),
    kpi("Critical / High", d.incidents.filter(x => x.severity === "CRITICAL" || x.severity === "HIGH").length),
  ];
  if (i.failures !== undefined) cards.push(kpi("Failed logins (last scan)", i.failures));
  if (i.successes !== undefined) cards.push(kpi("Remote logins (last scan)", i.successes));
  document.getElementById("stats").replaceChildren(...cards);

  renderView();

  rescanBtn.style.display = s.can_rescan ? "" : "none";
  range.style.display = s.can_rescan ? "" : "none";
  if (s.can_rescan && !rangeTouched && rangeFor !== i.hours) { fillRange(i.hours); rangeFor = i.hours; }
  range.disabled = s.status === "running";
  rescanBtn.disabled = s.status === "running";
  rescanBtn.textContent = s.status === "running" ? "Scanning..." : "Rescan now";
  if (s.status === "running") setTimeout(load, 2000);

  document.getElementById("updated").textContent = "Updated " + new Date().toLocaleTimeString();
}

function setLive(on, text) {
  document.getElementById("live").className = "pill" + (on ? "" : " off");
  document.getElementById("livetext").textContent = text;
}

async function load() {
  try {
    const r = await fetch("/api/data?token=" + encodeURIComponent(token));
    if (!r.ok) throw new Error("HTTP " + r.status);
    render(await r.json());
    setLive(!ui.paused, ui.paused ? "PAUSED" : "LIVE");
  } catch (e) {
    document.getElementById("updated").textContent = "Could not load data: " + e.message;
    setLive(false, "OFFLINE");
  }
}

async function rescan() {
  rescanBtn.disabled = true;
  range.disabled = true;
  const q = range.value ? "&hours=" + encodeURIComponent(range.value) : "";
  try { await fetch("/api/rescan?token=" + encodeURIComponent(token) + q, {method: "POST"}); } catch (e) {}
  load();
}

const actions = document.getElementById("actions");
const rescanBtn = el("button", "Rescan now", "btn primary");
rescanBtn.style.display = "none";
rescanBtn.onclick = rescan;
const RANGES = [[1, "Last hour"], [6, "Last 6 hours"], [24, "Last 24 hours"], [72, "Last 3 days"], [168, "Last 7 days"]];
const range = el("select", null, "select");
range.setAttribute("aria-label", "How far back the next scan should look");
range.title = "How far back to scan";
range.style.display = "none";
let rangeTouched = false, rangeFor = null;
function fillRange(current) {
  const list = RANGES.slice(), cur = Number(current) || 24;
  if (!list.some(r => r[0] === cur)) list.push([cur, "Last " + cur + " hours"]);
  range.replaceChildren(...list.map(([v, label]) => { const o = el("option", label); o.value = String(v); return o; }));
  range.value = String(cur);
}
fillRange(24);
range.onchange = () => { rangeTouched = true; rescan(); };
actions.appendChild(range);
actions.appendChild(rescanBtn);

const pauseBtn = el("button", "Pause", "btn");
pauseBtn.title = "Stop the page from refreshing by itself";
pauseBtn.onclick = () => {
  ui.paused = !ui.paused;
  pauseBtn.textContent = ui.paused ? "Resume" : "Pause";
  setLive(!ui.paused, ui.paused ? "PAUSED" : "LIVE");
  if (!ui.paused) load();
};
actions.appendChild(pauseBtn);

["csv", "html", "json"].forEach(kind => {
  const a = el("a", "Download " + kind.toUpperCase(), "btn");
  a.href = "/download/" + kind + "?token=" + encodeURIComponent(token);
  actions.appendChild(a);
});

const helpBtn = el("button", "? Help", "btn");
helpBtn.title = "What do these words and colours mean?  (press ?)";
helpBtn.onclick = openHelp;
actions.appendChild(helpBtn);

const themeBtn = el("button", "", "btn");
function currentTheme() { return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark"; }
function applyTheme(t, save) {
  document.documentElement.setAttribute("data-theme", t);
  themeBtn.textContent = t === "dark" ? "☀ Light" : "☾ Dark";
  themeBtn.title = t === "dark" ? "Switch to the light theme" : "Switch to the dark theme";
  if (save) { try { localStorage.setItem("ls-theme", t); } catch (e) {} }
}
themeBtn.onclick = () => applyTheme(currentTheme() === "dark" ? "light" : "dark", true);
applyTheme(currentTheme(), false);
actions.appendChild(themeBtn);

const search = document.getElementById("q");
search.addEventListener("input", () => { ui.q = search.value; renderView(); });
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && panelOpen()) { closePanel(); return; }
  const typing = ["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName);
  if (e.key === "?" && !typing) { e.preventDefault(); openHelp(); return; }
  if (e.key === "/" && !typing) {
    e.preventDefault();
    if (ui.tab === "overview") setTab("alerts");
    search.focus();
  } else if (e.key === "Escape" && document.activeElement === search) {
    search.value = ""; ui.q = ""; search.blur(); renderView();
  }
});

const startTab = location.hash.replace("#", "");
if (["overview", "incidents", "alerts"].includes(startTab)) ui.tab = startTab;

load();
setInterval(() => { if (!ui.paused) load(); }, 10000);
</script></body></html>
"""
