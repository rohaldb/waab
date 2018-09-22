import React, { Component } from 'react'
import Dropzone from 'react-dropzone'

class App extends Component {
  state = { files: [] }

  onDrop (files) {
    this.setState({
      files
    })
  }

  sendFile = () => {
    var data = new FormData()
    data.append('file', this.state.files[0])
    data.append('user', 'hubot')
    
    fetch('http://localhost:5000/', { // Your POST endpoint
      method: 'POST',
      // headers: {
      //   "Content-Type": "You will perhaps need to define a content-type here"
      // },
      body: data
    }).then(response => {
      console.log('responded ', response)
      // response.json() // if the response is a JSON object
    }).catch(
      error => console.error(error) // Handle the error response object
    )
  }

  render () {
    return (
      <div className='App'>
        <section>
          <div className='dropzone'>
            <Dropzone onDrop={this.onDrop.bind(this)} multiple={false}>
              <p>Drag a file here or click.</p>
            </Dropzone>
          </div>
          <aside>
            <h2>Dropped files</h2>
            <ul>
              {
              this.state.files.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
            }
            </ul>
          </aside>
        </section>
        <p onClick={() => this.sendFile()}>Go!</p>
      </div>
    )
  }
}

export default App
