const Panaroma = () => {
  const buttons = {
    site: 0,
    screenshot: false,
    stitch: false,
  }

  const changeSite = (site) => {
    buttons.site = site
    console.log(buttons)
  }

  const sendReq = (type) => {
    const res = buttons

    if (type === 'screenshot') {
      res.stitch = false
      res.screenshot = true
    } else if (type === 'camera switch') {
    } else {
      res.stitch = true
      res.screenshot = false
    }
    // publish to an end point
  }

  return (
    <>
      <div>
        <button onClick={() => changeSite(1)}>Site 1</button>
        <button onClick={() => changeSite(2)}>Site 2</button>
        <button onClick={() => changeSite(3)}>Site 3</button>
        <button onClick={() => changeSite(4)}>Site 4</button>
      </div>
      <img
        src='http://localhost:5000/video_feed'
        alt='Video'
        style={{ width: '100%', height: '88%' }}
      />
      <div>
        <button onClick={() => sendReq('screenshot')}>Screenshot</button>
        <button onClick={() => sendReq('stitch')}>Stitch Image</button>
        <button onClick={() => sendReq('camera switch')}>Switch Camera</button>
      </div>
    </>
  )
}

export default Panaroma
