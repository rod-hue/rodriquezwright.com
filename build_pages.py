import os
#!/usr/bin/env python3
"""Builds the deep pages of rodriquezwright.com: /about/, /campaigns/, /publisher/, /rod212/.
Facts come from the Wikipedia draft (sourced). Third-person voice, no em dashes."""
import json, os

SITE = 'https://rodriquezwright.com'
PERSON = SITE + '/#person'
NAV = [('About', '/about/'), ('Campaigns', '/campaigns/'), ('Publisher', '/publisher/'), ('Writing', '/writing/'), ('Guides', '/guides/'), ('Photography', '/photography/'), ('Rod212', '/rod212/'), ('Work with him', '/#hire')]

CSS = """
:root{--bg:#0a0a0b;--bg2:#111113;--ink:#f3efe6;--dim:#a19c92;--faint:#5c5850;--line:rgba(243,239,230,.12);--gold:#d4a957;--gold2:#f0cf8a;
--serif:"Instrument Serif",Georgia,serif;--sans:"Inter Tight",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;--pad:clamp(16px,4vw,56px)}
*{box-sizing:border-box;margin:0;padding:0}html{background:var(--bg)}body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:18px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%;display:block}
.top{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:16px var(--pad);background:rgba(10,10,11,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.top .mark{font-family:var(--serif);font-size:24px;text-decoration:none;letter-spacing:.02em}
.top ul{list-style:none;display:flex;gap:clamp(12px,2vw,28px);flex-wrap:wrap}.top li a{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);text-decoration:none}
.top li a:hover,.top li a[aria-current]{color:var(--gold2)}
.hero{position:relative;min-height:72vh;display:grid;align-items:end;overflow:hidden;isolation:isolate}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 12%;z-index:-2;filter:saturate(.95)}
@media (min-width:900px){.hero img{left:auto;width:44%;object-position:50% 18%}.hero::after{background:linear-gradient(90deg,var(--bg) 52%,rgba(10,10,11,.35) 70%,rgba(10,10,11,0)),linear-gradient(0deg,var(--bg) 2%,transparent 30%)!important}.hero-in{max-width:58%}}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,var(--bg) 4%,rgba(10,10,11,.55) 45%,rgba(10,10,11,.15))}
.hero-in{padding:0 var(--pad) clamp(40px,7vh,80px);max-width:1200px}
.kick{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2)}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(52px,8vw,120px);line-height:.95;letter-spacing:-.01em;margin:14px 0 18px}
h1 em,h2 em{color:var(--gold2)}
.dek{font-size:clamp(18px,1.6vw,22px);color:var(--dim);max-width:720px}
main{max-width:780px;margin:0 auto;padding:clamp(40px,7vh,90px) var(--pad)}
main h2{font-family:var(--serif);font-weight:400;font-size:clamp(34px,4vw,52px);line-height:1.05;margin:56px 0 16px}
main h3{font-family:var(--mono);font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold2);margin:34px 0 10px}
main p{margin:0 0 18px;color:#e6e1d6}main p a{color:var(--gold2);text-underline-offset:3px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:30px 0}
.facts div{background:var(--bg2);padding:18px 20px}.facts b{display:block;font-family:var(--serif);font-weight:400;font-size:30px;color:var(--gold2);line-height:1.1}.facts span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}
/* writing */.w-list{display:grid;gap:14px;margin:10px 0 30px}.w-item{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:var(--bg2)}.w-item h3{margin:6px 0 6px;font-family:var(--serif);font-weight:400;font-size:25px;line-height:1.2;text-transform:none;letter-spacing:0;color:#f3efe6}.w-item h3 a{color:inherit;text-decoration:none}.w-item h3 a:hover{color:var(--gold2)}.w-item p{margin:0;color:var(--dim);font-size:15px}
.ph-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:18px 0 34px}.ph-grid figure{margin:0;border-radius:12px;overflow:hidden;background:var(--bg2);position:relative;aspect-ratio:4/5}.ph-grid img{width:100%;height:100%;object-fit:cover;object-position:50% 25%;display:block}.ph-grid figcaption{position:absolute;left:8px;bottom:8px;padding:4px 9px;border-radius:999px;background:rgba(0,0,0,.6);font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:#f3efe6}
ul.list{margin:0 0 18px 1.2em}ul.list li{margin:6px 0;color:#e6e1d6}
.src{border-top:1px solid var(--line);margin-top:60px;padding-top:22px}.src h3{margin-top:0}.src li{font-size:14.5px;color:var(--dim);margin:6px 0}
.next{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:50px}
.next a{display:block;padding:22px;border:1px solid var(--line);border-radius:14px;text-decoration:none;transition:border-color .3s,transform .3s}.next a:hover{border-color:var(--gold);transform:translateY(-3px)}
.next span{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}.next b{display:block;font-family:var(--serif);font-weight:400;font-size:26px;margin-top:6px}
footer{border-top:1px solid var(--line);padding:30px var(--pad);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
footer a{color:var(--dim);text-decoration:none}
@media (max-width:700px){.top ul{display:none}body{font-size:17px}}
.disco{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:18px;margin:26px 0}
.disco details{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--bg2)}
.disco summary{list-style:none;cursor:pointer}.disco summary::-webkit-details-marker{display:none}
.disco img{width:100%;aspect-ratio:1;object-fit:cover;background:#1a1a1d}
.disco .t{display:block;padding:10px 12px 2px;font-size:14.5px;line-height:1.3;font-weight:600}
.disco .y{display:block;padding:0 12px 12px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}
.disco ol{margin:0;padding:4px 12px 12px 30px;font-size:13.5px;color:#e6e1d6}.disco ol li{margin:4px 0}.disco ol a{color:var(--gold2);text-decoration:none}
.disco .go{display:block;padding:0 12px 12px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold2);text-decoration:none}
"""

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def discography():
    rel = json.load(open('data/discography.json'))
    cards = []
    for r in rel:
        kind = 'Single' if r['count'] == 1 else ('EP' if r['count'] <= 6 else 'Album')
        title = r['title'].replace(' - Single', '').replace(' - EP', '')
        who = '' if r['artist'] == 'Rod212' else f' &middot; {esc(r["artist"])}'
        tracks = ''.join(f'<li><a href="{t["url"]}" rel="noopener">{esc(t["title"])}</a></li>' for t in r['tracks'])
        cards.append(f'<details><summary><img src="{r["art"]}" alt="{esc(title)} cover art" loading="lazy" width="400" height="400">'
                     f'<span class="t">{esc(title)}</span><span class="y">{r["date"][:4]} &middot; {kind}{who}</span></summary>'
                     f'<ol>{tracks}</ol><a class="go" href="{r["url"]}" rel="noopener">Open in Apple Music</a></details>')
    n_tracks = sum(len(r['tracks']) for r in rel)
    ld = {"@context": "https://schema.org", "@type": "MusicGroup", "@id": SITE + '/rod212/#artist', "name": "Rod212",
          "url": SITE + '/rod212/', "member": {"@id": PERSON}, "foundingLocation": "Chicago, Illinois",
          "sameAs": ["https://music.apple.com/us/artist/1066113726", "https://open.spotify.com/artist/1VtIRrcWyxHXd5Fe2iEaRg",
                     "https://www.youtube.com/@Rod212Official", "https://musicbrainz.org/artist/97c666a3-d5a9-4b33-b8d0-c6ee26b16345",
                     "https://www.discogs.com/artist/10982258-Rod212", "https://genius.com/artists/Rod212", "https://www.bandsintown.com/a/15671105",
        "https://www.wikidata.org/wiki/Q141780060"],
          "album": [{"@type": "MusicAlbum", "name": r['title'], "datePublished": r['date'], "url": r['url'], "image": r['art'],
                     "numTracks": r['count'], "byArtist": {"@type": "MusicGroup", "name": r['artist']},
                     "track": [{"@type": "MusicRecording", "name": t['title'], "url": t['url']} for t in r['tracks']]} for r in rel]}
    return (f'<h2>The full <em>discography</em></h2>'
            f'<p>Every Rod212 release on Apple Music, newest first: {len(rel)} releases and {n_tracks} tracks. Tap a cover to see its tracks.</p>'
            f'<div class="disco">{"".join(cards)}</div>'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

def page(slug, title, desc, kicker, h1, dek, img, img_alt, body, sources, about_type='AboutPage'):
    url = f'{SITE}/{slug}/'
    nav = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == "/" + slug + "/" else ""}>{n}</a></li>' for n, h in NAV)
    others = [(n, h) for n, h in NAV[:6] if h != '/' + slug + '/']
    nxt = ''.join(f'<a href="{h}"><span>Rodriquez Wright II</span><b>{n}</b></a>' for n, h in others)
    src = ''.join(f'<li><a href="{u}" rel="noopener">{t}</a></li>' if u else f'<li>{t}</li>' for t, u in sources)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": [about_type, "WebPage"] if about_type != 'WebPage' else "WebPage", "@id": url + '#page', "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": SITE + '/#website'}, "about": {"@id": PERSON}, "mainEntity": {"@id": PERSON},
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + '/' + img}},
        {"@type": "WebSite", "@id": SITE + '/#website', "url": SITE + '/', "name": "Rodriquez Wright II"},
        {"@type": "Person", "@id": PERSON, "name": "Rodriquez Wright II", "alternateName": ["Rod Wright", "Rod212", "Rodriquez Wright", "Rodriguez Wright", "Rodriguez Wright II", "Rod Wright II"], "url": SITE + '/'},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Rodriquez Wright II", "item": SITE + '/'},
            {"@type": "ListItem", "position": 2, "name": h1.replace('<em>', '').replace('</em>', ''), "item": url}]}]}
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="author" content="Rodriquez Wright II">
<meta name="theme-color" content="#0a0a0b">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Rodriquez Wright II">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="profile:first_name" content="Rodriquez"><meta property="profile:last_name" content="Wright">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;600;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><a class="mark" href="/">Rodriquez Wright II</a><nav aria-label="Pages"><ul>{nav}</ul></nav></header>
<section class="hero"><img src="/{img}" alt="{img_alt}"><div class="hero-in"><span class="kick">{kicker}</span><h1>{h1}</h1><p class="dek">{dek}</p></div></section>
<main>
{body}
<div class="next">{nxt}</div>
<div class="src"><h3>Sources</h3><ul>{src}</ul></div>
</main>
<footer><span>&copy; 2026 Rodriquez Wright II</span><span><a href="/">rodriquezwright.com</a> &middot; <a href="https://leooperations.com/team/rodriquez-wright-ii/">Leo Operations</a> &middot; <a href="https://www.washingtondcmagazine.com/author/rod/">Washington DC Magazine</a> &middot; <a href="https://about.me/rodriquezwrightii">About.me</a></span></footer>
</body>
</html>
"""
    os.makedirs(slug, exist_ok=True)
    open(os.path.join(slug, 'index.html'), 'w').write(html)
    return url

SJR = ('Tennessee General Assembly, Senate Joint Resolution 905 (2012)', 'https://www.capitol.tn.gov/Bills/107/Bill/SJR0905.pdf')
LEO = ('Leo Operations, team page: Rodriquez Wright II', 'https://leooperations.com/team/rodriquez-wright-ii/')
WDCM = ('Washington DC Magazine, author page', 'https://www.washingtondcmagazine.com/author/rod/')

urls = []

urls.append(page('about', 'About Rodriquez Wright II | Strategist, Publisher, Artist',
  'Rodriquez Wright II is a Nashville-based political strategist, founder of Leo Operations, publisher of Washington DC Magazine and the recording artist Rod212.',
  'About', 'Rodriquez <em>Wright II</em>', 'Political strategist. Publisher. Recording artist. One person behind three very different rooms.',
  'img/rodriquez-wright-ii-portrait.jpg', 'Rodriquez Wright II',
  """
<p><strong>Rodriquez Wright II</strong>, known as <strong>Rod Wright</strong> (his first name is often misspelled "Rodriguez"), is an American political organizer, media entrepreneur and hip-hop recording artist based in Nashville, Tennessee. He founded the political consulting and media firm <a href="https://leooperations.com/">Leo Operations</a>, he is the founder and editor-in-chief of <a href="https://www.washingtondcmagazine.com/">Washington DC Magazine</a>, and he records and produces music under the name <a href="/rod212/">Rod212</a>.</p>
<div class="facts"><div><b>14 years</b><span>in campaigns</span></div><div><b>25 states</b><span>worked</span></div><div><b>1,000+</b><span>events photographed</span></div><div><b>2.8M+</b><span>Spotify streams as Rod212</span></div></div>
<h2>Early life and <em>education</em></h2>
<p>Wright grew up in Chicago and moved to Nashville to attend <strong>Tennessee State University</strong>, the historically Black university, where he studied English and was named to the dean's list. He went on to earn a Master of Public Administration at Tennessee State.</p>
<p>His first job in politics came at the State Capitol. During the 2012 session of the 107th Tennessee General Assembly he served as a legislative intern for State Senator Ophelia Ford. The legislature recognized that work in <a href="https://www.capitol.tn.gov/Bills/107/Bill/SJR0905.pdf">Senate Joint Resolution 905</a>, which commended him for his service. He also interned with the Tennessee Democratic Party.</p>
<h2>A career in <em>three parts</em></h2>
<h3>The strategist</h3>
<p>Since 2012 Wright has organized, managed and advised campaigns from Nashville school board races to statewide ballot measures and a presidential primary. He was Tennessee organizing director for Michael Bloomberg's 2020 presidential campaign, managed Nashville District Attorney Glenn Funk's 2022 re-election, and has directed field programs in more than two dozen states. The full record is on the <a href="/campaigns/">campaigns page</a>.</p>
<h3>The publisher</h3>
<p>Wright founded Washington DC Magazine, an independent publication covering politics, business, culture and the people shaping the capital, and he serves as its editor-in-chief. He reports and photographs for the magazine himself, and he is a member of the National Association of Black Journalists. More on the <a href="/publisher/">publisher page</a>.</p>
<h3>The artist</h3>
<p>As Rod212, Wright writes, produces and shoots independent hip-hop and R&amp;B. His songs have passed 2.8 million streams on Spotify, and his music has been covered by The Source, EarMilk and Wordplay Magazine. More on the <a href="/rod212/">Rod212 page</a>.</p>
<h2>Behind the <em>camera</em></h2>
<p>Much of Leo Operations' work is visual. Wright has photographed more than 1,000 events, from campaign launches and legislative sessions to galas and HBCU homecomings, and the firm's photo and video clients have included Nashville Mayor Freddie O'Connell, members of the Tennessee General Assembly, the Memphis Grizzlies, the National Black Caucus of State Legislators and Meharry Medical College.</p>
""", [SJR, LEO, WDCM, ('The Source, "Rod212 Continues His 2022 Dominance With Pro-Humanity Single Social Privilege" (Oct 21, 2022)', 'https://thesource.com/2022/10/21/rod212-continues-his-2022-dominance-with-pro-humanity-single-social-privilege/')], 'ProfilePage'))

urls.append(page('campaigns', 'Rodriquez Wright II | Political Strategist and Campaign Manager',
  'The political career of Rodriquez Wright II: Nashville races, national field programs, Bloomberg 2020 in Tennessee, and campaign management through Leo Operations.',
  'The strategist', 'Fourteen years in <em>campaigns</em>', 'From a Nashville school board race to a presidential primary, the record of a field organizer turned campaign manager.',
  'img/capitol.jpg', 'Rodriquez Wright II at the U.S. Capitol',
  """
<p>Rodriquez Wright II has worked in campaigns since 2012, first in Nashville, then across the country as a field director, and now through his own firm, <a href="https://leooperations.com/">Leo Operations</a>. His work centers on field organizing, voter contact and campaign management.</p>
<h2>Nashville, <em>2012 to 2015</em></h2>
<p>Wright started while still a student at Tennessee State University. In 2012 he was a Davidson County field organizer for the Tennessee Democratic Party and a field organizer for Sharon Gentry's re-election to the Metro Nashville school board, where Gentry defeated 27-year incumbent Ed Kindall. From 2013 to 2015 he worked for the Nashville public affairs firm Calvert Street Group. In 2014 he managed Allegra Walker's campaign for Davidson County General Sessions judge and consulted for Kelvin Jones's campaign for Circuit Court judge.</p>
<p>In 2015 he was deputy campaign manager and then campaign manager for former vice mayor Howard Gentry's campaign for mayor of Nashville, then community outreach director for David Fox in the September runoff.</p>
<h2>National field work, <em>2015 to 2020</em></h2>
<p>From 2015 to 2016 Wright was a campaign associate with Revolution Field Strategies, a Boston canvassing firm, directing petition drives and canvass programs in several states. They included the signature drive for a Massachusetts ballot initiative on hospital prices and the drive for Montana's I-181 brain research bond program. He also worked on Hillary Clinton's 2016 New Hampshire primary campaign.</p>
<ul class="list">
<li><strong>2017:</strong> field director for canvassing on Kansas City's $800 million general obligation bond package, which voters approved.</li>
<li><strong>2017 to 2018:</strong> campaign manager for Omar Passons's campaign for the San Diego County Board of Supervisors.</li>
<li><strong>2018:</strong> directed petition drives for Arizona's Invest in Ed initiative, which submitted about 270,000 signatures, and for the one-cent transportation tax in Hillsborough County, Florida, which voters approved.</li>
<li><strong>2018:</strong> Tennessee state project director for BlackPAC.</li>
<li><strong>2019:</strong> directed the Chicago canvass for The Black Institute's #KeepStarz campaign.</li>
<li><strong>December 2019:</strong> named Tennessee organizing director for Michael Bloomberg's 2020 presidential campaign, which opened its state headquarters in Nashville that month.</li>
</ul>
<h2>Leo <em>Operations</em></h2>
<p>Wright founded Leo Operations, a Nashville firm providing campaign management, field strategy, media production and digital marketing for campaigns, elected officials, nonprofits and businesses. Through the firm he was campaign manager for District Attorney Glenn Funk's 2022 re-election, and digital consultant to Metro Council at-large members Zulfat Suara and Burkley Allen in 2019 and 2023. In 2023 Suara and Allen were re-elected as part of the first at-large Metro Council delegation made up entirely of women. He is also digital consultant to Sharon Hurt's 2026 campaign for Davidson County Clerk.</p>
<p>In 2023 the firm was a field consultant for SEIU Virginia during that year's Virginia General Assembly elections. Its photo and video clients have included Nashville Mayor Freddie O'Connell, state legislators Justin Jones, London Lamar, Charlane Oliver, Gloria Johnson, Jesse Chism and Heidi Campbell, and Dan Osborn's 2024 U.S. Senate campaign in Nebraska.</p>
""", [LEO, SJR]))

urls.append(page('publisher', 'Rodriquez Wright II | Founder and Editor-in-Chief, Washington DC Magazine',
  'Rodriquez Wright II founded Washington DC Magazine and serves as its editor-in-chief: politics, business, culture and the people shaping the capital.',
  'The publisher', 'Washington DC <em>Magazine</em>', 'Founder and editor-in-chief of an independent magazine from the nation’s capital.',
  'img/hall.jpg', 'Rodriquez Wright II',
  """
<p>Rodriquez Wright II is the founder and editor-in-chief of <a href="https://www.washingtondcmagazine.com/">Washington DC Magazine</a>, an independent digital publication covering politics, business, culture, sports and lifestyle in Washington, D.C., Northern Virginia and suburban Maryland, with a national lens on the people and decisions that come out of the capital.</p>
<h2>What the magazine <em>covers</em></h2>
<p>Its coverage areas include federal and local politics, Black culture and nightlife, Howard University and other historically Black colleges and universities, and a Gen Z DC section on the city's younger residents. The magazine publishes <strong>The DC Insider</strong>, a newsletter, and <strong>The District Daily</strong>, a collection of free daily puzzle games built around the city.</p>
<h2>The editor's <em>role</em></h2>
<p>As editor-in-chief, Wright sets the publication's editorial direction and standards, and he reports and photographs stories himself. He is a member of the National Association of Black Journalists.</p>
<p>In September 2026 he covered the Congressional Black Caucus Foundation's 50th Phoenix Awards Dinner, which closed its Annual Legislative Conference. For that story he interviewed honoree Viola Davis and Representative Ilhan Omar of Minnesota about the next generation of Black political leadership.</p>
<h2>Where campaigns meet <em>the newsroom</em></h2>
<p>Wright came to publishing from campaigns, and the magazine reflects that: it covers power the way an organizer sees it, through the people on the ground as well as the officials at the podium. His reporting and photography appear on his <a href="https://www.washingtondcmagazine.com/author/rod/">author page</a>.</p>
""", [WDCM, ('Washington DC Magazine', 'https://www.washingtondcmagazine.com/')]))

urls.append(page('rod212', 'Rod212 | Music by Rodriquez Wright II',
  'Rod212 is the music of Rodriquez Wright II: independent hip-hop and R&B, self-produced, 2.8 million Spotify streams, covered by The Source, EarMilk and Wordplay.',
  'The artist', 'Rod<em>212</em>', 'The music of Rodriquez Wright II. Independent, self-produced, and shot by the artist himself.',
  'img/hero.jpg', 'Rodriquez Wright II, known as Rod212',
  """
<p><strong>Rod212</strong> is the stage name of Rodriquez Wright II, an independent hip-hop and R&amp;B artist, producer and filmmaker from Chicago, now based in Nashville. He releases his music on his own Rod212 imprint and writes, produces and shoots his own work.</p>
<div class="facts"><div><b>2.8M+</b><span>Spotify streams, top songs</span></div><div><b>815K</b><span>For The Summer</span></div><div><b>4.3M</b><span>TikTok views on For The Summer</span></div><div><b>170+</b><span>credits on Muso.ai</span></div></div>
<h2>The <em>releases</em></h2>
<p>His early singles included "Trained to Go" (2021), with Jesse LeProtti and YSN Flow, and "Too Much" and "For The Summer" (2022). "For The Summer" spread on TikTok, where creators' videos using the song drew millions of views, and it has since passed 800,000 Spotify streams.</p>
<p>His 2022 single "Social Privilege," which addresses the history of slavery and racism and their present-day effects, was covered by <a href="https://thesource.com/2022/10/21/rod212-continues-his-2022-dominance-with-pro-humanity-single-social-privilege/">The Source</a>. In 2023 he released a run of singles including "She Was Like," "Gone," "Two Cups" and "Really Not Okay"; the last, featuring Sal Ly and Rico Maz, was covered by <a href="https://earmilk.com/2023/01/28/rod212-offers-up-an-anthem-for-love-and-heartbreak-on-really-not-okay/">EarMilk</a> and <a href="https://www.wordplaymagazine.com/blog-1/2023/1/31/rod212-ft-sal-ly-rico-maz-really-not-okay-single">Wordplay Magazine</a>.</p>
<p>In 2024 he released "She Right There" with Evan Joseph, and in 2025 he released "Monday" with an official music video that is closing in on one million YouTube views. His other music videos include "On The Water," "Expensive Love" and "Wind It," featuring Young Dave.</p>
<h2>Listen and <em>watch</em></h2>
<ul class="list">
<li><a href="https://open.spotify.com/artist/1VtIRrcWyxHXd5Fe2iEaRg">Spotify</a></li>
<li><a href="https://music.apple.com/us/artist/1066113726">Apple Music</a></li>
<li><a href="https://www.youtube.com/@Rod212Official">YouTube</a></li>
<li><a href="https://soundcloud.com/rod212">SoundCloud</a></li>
<li><a href="https://www.instagram.com/rod212/">Instagram</a></li>
<li><a href="https://genius.com/artists/Rod212">Genius</a> (lyrics)</li>
<li><a href="https://www.bandsintown.com/a/15671105">Bandsintown</a> (shows)</li>
<li><a href="https://www.discogs.com/artist/10982258-Rod212">Discogs</a> and <a href="https://musicbrainz.org/artist/97c666a3-d5a9-4b33-b8d0-c6ee26b16345">MusicBrainz</a> (discography data)</li>
</ul>
""" + discography() + """
<h2>One artist, <em>two names</em></h2>
<p>Off the mic, Rod212 is Rodriquez Wright II: political strategist, founder of Leo Operations and publisher of Washington DC Magazine. Read the full story on the <a href="/about/">about page</a>.</p>
""", [('The Source (Oct 21, 2022)', 'https://thesource.com/2022/10/21/rod212-continues-his-2022-dominance-with-pro-humanity-single-social-privilege/'),
      ('EarMilk (Jan 28, 2023)', 'https://earmilk.com/2023/01/28/rod212-offers-up-an-anthem-for-love-and-heartbreak-on-really-not-okay/'),
      ('Wordplay Magazine (Jan 31, 2023)', 'https://www.wordplaymagazine.com/blog-1/2023/1/31/rod212-ft-sal-ly-rico-maz-really-not-okay-single'),
      ('Mystic Sons, "Getting To Know... Rod212" (Jan 30, 2023)', 'https://www.mysticsons.com/article/getting-know-rod212'),
      ('Muso.ai credits profile', 'https://muso.ai/profile/fe1684e2-ac56-4df6-b3e9-57a88d01f90d')], 'WebPage'))

import json as _j
_A = _j.load(open('data/wdcm_articles.json'))
def _writing_body():
    items = ''.join(f'<article class="w-item"><span class="kick">{esc(a["date"][:4])} &middot; Washington DC Magazine</span><h3><a href="{a["url"]}">{esc(a["title"])}</a></h3><p>{esc(a["excerpt"])}</p></article>' for a in _A)
    return f"""
<p>Rodriquez Wright II reports, interviews and photographs for <a href="https://www.washingtondcmagazine.com/">Washington DC Magazine</a>, the publication he founded and edits. Below is his bylined work, newest first. The full archive lives on his <a href="https://www.washingtondcmagazine.com/author/rod/">author page</a>.</p>
<div class="facts"><div><b>{len(_A)}</b><span>bylined stories</span></div><div><b>Politics</b><span>Congress and the CBC</span></div><div><b>Culture</b><span>artists and interviews</span></div><div><b>DC</b><span>local coverage</span></div></div>
<h2>Bylined <em>stories</em></h2>
<div class="w-list">{items}</div>
<h2>On the <em>beat</em></h2>
<p>His reporting covers Congress and the Congressional Black Caucus, Washington's arts scene, independent musicians and the people shaping the capital. He also writes the magazine's editor's notes.</p>
"""
urls.append(page('writing', 'Rodriquez Wright II | Articles and Interviews, Washington DC Magazine',
  'Articles, interviews and reporting by Rodriquez Wright II (Rod Wright), founder and editor-in-chief of Washington DC Magazine: politics, the CBC, artists and DC culture.',
  'The writer', 'Articles and <em>interviews</em>', 'Reporting and interviews by Rodriquez Wright II for Washington DC Magazine.',
  'img/hall.jpg', 'Rodriquez Wright II', _writing_body(), [WDCM, ('Washington DC Magazine', 'https://www.washingtondcmagazine.com/')], 'CollectionPage'))

import glob as _g, re as _re
def _load_guides():
    out = []
    for f in sorted(_g.glob(os.path.expanduser('~/projects/leooperations-site/_src/guides/md/*.md'))):
        m = _re.match(r'^---\n(.*?)\n---\n', open(f).read(), _re.S)
        if not m: continue
        d = dict((l.split(':', 1)[0].strip(), l.split(':', 1)[1].strip()) for l in m.group(1).split('\n') if ':' in l)
        out.append(d)
    return out
_G = _load_guides()
_GCATS = ['Campaigns', 'Field', 'Media', 'Organizing', 'Weddings']
def _guides_body():
    secs = ''
    for c in _GCATS:
        items = ''.join(f'<article class="w-item"><span class="kick">{esc(c)} &middot; Leo Operations</span><h3><a href="https://leooperations.com/guides/{g["slug"]}/">{esc(g["h1"])}</a></h3><p>{esc(g.get("dek",""))}</p></article>' for g in _G if g.get('category') == c)
        if items: secs += f'<h2>{esc(c)}</h2><div class="w-list">{items}</div>'
    return f"""
<p>Rodriquez Wright II wrote these {len(_G)} in-depth guides for <a href="https://leooperations.com/">Leo Operations</a>, the national field, media and creative firm he founded in 2019. They draw on political campaign work going back to 2012: running for office, building a campaign budget, voter registration and get-out-the-vote programs, political TV and digital advertising, organizing events, and wedding photography and film.</p>
<div class="facts"><div><b>{len(_G)}</b><span>guides</span></div><div><b>650,000+</b><span>doors knocked by Leo field programs</span></div><div><b>25</b><span>states with campaign work</span></div><div><b>1,000+</b><span>events photographed</span></div></div>
{secs}
<p>Browse every guide on the <a href="https://leooperations.com/guides/">Leo Operations guides page</a>.</p>
"""
if _G:
    urls.append(page('guides', 'Rodriquez Wright II | Guides on Campaigns, Field, Media and Weddings',
      'In-depth guides by Rodriquez Wright II (Rod Wright) for Leo Operations: campaign costs and budgets, voter registration, GOTV, political ads, organizing events and wedding photo and film.',
      'The guides', 'Guides by <em>Rodriquez Wright II</em>', 'In-depth guides on campaigns, field, media, organizing and weddings, written for Leo Operations.',
      'img/hall.jpg', 'Rodriquez Wright II', _guides_body(), [('Leo Operations guides', 'https://leooperations.com/guides/')], 'CollectionPage'))

_SHOT = [('beyonce','Beyoncé'),('metgala','The Met Gala'),('jayz','JAY-Z'),('jeezy','Jeezy'),('warnock','Sen. Raphael Warnock'),('patti','Patti LaBelle'),('sharpton','Rev. Al Sharpton'),('booker','Sen. Cory Booker'),('paris','Paris Hilton'),('firsttake','ESPN First Take'),('ludacris','Ludacris'),('carmelo','Carmelo Anthony')]
def _photo_body():
    grid = ''.join(f'<figure><img src="/img/shot/{s}.jpg" alt="{esc(n)} photographed by Rod Wright" loading="lazy"><figcaption>{esc(n)}</figcaption></figure>' for s, n in _SHOT)
    return f"""
<p><strong>Rod Wright</strong>, legally Rodriquez Wright II, is a photographer and filmmaker based in Nashville who has photographed more than 1,000 events. His work spans red carpets, concerts, political campaigns, galas, HBCU homecomings and weddings, and it runs through <a href="https://leooperations.com/">Leo Operations</a>, the media firm he founded, and <a href="https://www.washingtondcmagazine.com/">Washington DC Magazine</a>, where he shoots his own stories.</p>
<div class="facts"><div><b>1,000+</b><span>events photographed</span></div><div><b>56</b><span>films on YouTube</span></div><div><b>4K</b><span>cinema and drone</span></div><div><b>Nashville</b><span>and nationwide</span></div></div>
<h2>In the <em>room</em></h2>
<p>His lens has covered Beyoncé, JAY-Z, Patti LaBelle, Paris Hilton, Sen. Raphael Warnock, Sen. Cory Booker, Rev. Al Sharpton and the Met Gala.</p>
<div class="ph-grid">{grid}</div>
<h2>Events and <em>politics</em></h2>
<p>For campaigns and elected officials he shoots launches, swearing-ins, legislative sessions and election nights. Clients have included Nashville Mayor Freddie O'Connell, members of the Tennessee General Assembly, the National Black Caucus of State Legislators and the Memphis Grizzlies.</p>
<h2>Weddings</h2>
<p>Through Leo Operations, Wright and his team photograph and film weddings with coordinated photo, 4K video and drone coverage. See the <a href="https://leooperations.com/weddings/">wedding photography and film page</a> for recent couples and the highlight reel.</p>
<h2>See the <em>work</em></h2>
<ul class="list">
<li><a href="https://rodwrightphotography.pixieset.com/">Rod Wright Photography galleries</a> on Pixieset</li>
<li><a href="https://commons.wikimedia.org/wiki/Category:Photographs_by_Rod_Wright">Campaign photographs by Rod Wright</a> on Wikimedia Commons</li>
<li><a href="https://www.youtube.com/@leooperations">Leo Operations films</a> on YouTube</li>
<li><a href="https://www.instagram.com/rod212/">Instagram @rod212</a></li>
<li><a href="https://leooperations.com/nashville-photographer/">Book a Nashville event photographer</a> and <a href="https://leooperations.com/nashville-videographer/">videographer</a></li>
</ul>
"""
urls.append(page('photography', 'Rod Wright Photography | Rodriquez Wright II, Photographer and Filmmaker',
  'Rod Wright (Rodriquez Wright II) is a Nashville photographer and filmmaker: 1,000+ events, Beyoncé, JAY-Z, the Met Gala, campaigns, galas and weddings.',
  'The photographer', 'Rod Wright <em>Photography</em>', 'Red carpets, campaigns, concerts and weddings, through the lens of Rodriquez Wright II.',
  'photos/p01.jpg', 'Rod Wright behind the camera', _photo_body(), [LEO, WDCM, ('Rod Wright Photography on Pixieset', 'https://rodwrightphotography.pixieset.com/')], 'CollectionPage'))

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', f'  <url><loc>{SITE}/</loc><lastmod>2026-10-18</lastmod></url>']
sm += [f'  <url><loc>{u}</loc><lastmod>2026-10-18</lastmod></url>' for u in urls]
sm += ['</urlset>']
open('sitemap.xml', 'w').write('\n'.join(sm) + '\n')
print('\n'.join(urls))
