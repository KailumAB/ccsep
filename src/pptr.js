const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({args: ["--no-sandbox"]});
    const page = await browser.newPage();
    const navigationPromise = page.waitForNavigation();

    // Go to page and keep trying to login with admin creds until the server
    // is up
    while (true) {
        try {
            await page.goto("http://localhost:8000");
            await page.waitFor(500);
            break;
        } catch { continue; }
    }

    await page.type("#username", "admin");
    await page.type("#password", "strongpassword1337");
    await page.click("#submit");
    await page.waitForNavigation();

    while (true) {
        // Refresh the page every 10 seconds
        await page.waitFor(10000);
        try {
            await page.goto("http://localhost:8000");
        } catch { continue; }
    }

    await browser.close();
})();
