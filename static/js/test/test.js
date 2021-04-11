const expect = require('chai').expect;
const varsnap = require('varsnap');

const thirdparty = require('../thirdparty');
require('../fibonacci');

thirdparty.setupVarsnap();

context('Varsnap', function() {
  this.timeout(30 * 1000);
  it('runs with production', async function() {
    const status = await varsnap.runTests();
    expect(status).to.be.true;
  });
});
