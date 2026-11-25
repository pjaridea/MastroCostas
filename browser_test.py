from playwright.sync_api import sync_playwright
from pathlib import Path
import json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(offline=True,accept_downloads=True,viewport={'width':1280,'height':900}); page=c.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda x:x.accept())
 page.goto(Path('index.html').resolve().as_uri()); page.locator('[data-key=car]').fill('Test car');page.locator('[data-key=description]').fill('Test job');page.get_by_text('+ Ανταλλακτικό',exact=True).click();page.locator('[data-p=name]').fill('Test part');page.locator('[data-p=cost]').fill('50');page.locator('[data-key=hours]').fill('2');page.get_by_text('Αποθήκευση',exact=True).click();page.reload();page.get_by_text('Ιστορικό επισκευών',exact=True).click();assert page.get_by_text('Test car',exact=False).count();page.get_by_text('Άνοιγμα',exact=True).click();assert page.locator('[data-key=car]').input_value()=='Test car';page.evaluate('window.print=()=>{}');page.get_by_text('Δημιουργία προσφοράς',exact=True).click();assert 'Test part' in page.locator('#print').inner_text();page.emulate_media(media='print');assert page.locator('#print').is_visible();assert not page.locator('main').is_visible();page.pdf(path='/tmp/mastro-quote-test.pdf');page.emulate_media(media='screen');page.get_by_text('Ρυθμίσεις',exact=True).click();
 with page.expect_download() as event: page.get_by_text('Εξαγωγή JSON',exact=True).click()
 download=event.value;path='/tmp/mastro-backup-test.json';download.save_as(path);assert json.load(open(path))['history'][0]['car']=='Test car';page.get_by_text('Διαγραφή όλων',exact=True).click();page.locator('#importFile').set_input_files(path);page.wait_for_timeout(300);page.get_by_text('Ιστορικό επισκευών',exact=True).click();assert page.get_by_text('Test car',exact=False).count();page.get_by_text('Άνοιγμα',exact=True).click();page.locator('[data-key=status]').select_option('done');page.get_by_text('Αποθήκευση',exact=True).click();page.get_by_text('Οικονομική εικόνα',exact=True).click();assert page.get_by_text('Κέρδος ανά εργασία',exact=True).count();
 for width in [390,768,1280]:
  page.set_viewport_size({'width':width,'height':850});page.get_by_text('Νέα κοστολόγηση',exact=True).click();assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');
 assert not errors,errors
 print('PASS: Chromium offline, save/reload, backup/restore, print PDF, completed finance, 390/768/1280 px, no JS errors');b.close()
