import LogFit from 'logfit';
import Rollbar from 'rollbar';
import varsnap from 'varsnap';

import 'normalize.css/normalize.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';

export function setupRollbar() {
  const rollbarConfig = {
    accessToken: process.env.ROLLBAR_CLIENT_TOKEN,
    captureUncaught: true,
    payload: {
      environment: process.env.ENV,
    }
  };
  return Rollbar.init(rollbarConfig);
}

export function setupLogfit() {
  const logfit = new LogFit({
    source: process.env.LOGFIT_CLIENT_TOKEN,
  });
  logfit.report();
}

export function setupVarsnap() {
  varsnap.updateConfig({
    varsnap: 'true',
    env: process.env.ENV,
    producerToken: process.env.VARSNAP_PRODUCER_TOKEN,
    consumerToken: process.env.VARSNAP_CONSUMER_TOKEN,
  });
}

export function setupGoogleAnalytics() {
  const script = document.createElement('script');
  script.onload = function () {
    window.dataLayer = window.dataLayer || [];
    function gtag(){window.dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', process.env.GOOGLE_ANALYTICS_TOKEN);
  };
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + process.env.GOOGLE_ANALYTICS_TOKEN;
  document.head.appendChild(script);
}
