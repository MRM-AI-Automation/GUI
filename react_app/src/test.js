const util = require('util')

const exec = util.promisify(require('child_process').exec)

async function ping(hostname) {
  try {
    const { stdout, stderr } = await exec(`ping -c 1 ${hostname}`)
    console.log('stdout:', stdout)
    console.log('stderr:', stderr)
  } catch (err) {
    console.error(err)
  }
}

ping('10.0.0.0')
