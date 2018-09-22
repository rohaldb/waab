import React, {Component} from 'react'
import Dropzone from 'react-dropzone'
import Grid from '@material-ui/core/Grid'
import {withStyles} from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'
import {DataTable} from './components'

const styles = theme => ({})

class App extends Component {
  state = {
    files: []
  }

  onDrop(files) {
    this.setState({files})
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
    }).catch(error => console.error(error) // Handle the error response object
    )
  }

  render() {
    const {classes} = this.props

    return (
      <div className='App'>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="title" color="inherit" className={classes.grow}>
              WAAB
            </Typography>
          </Toolbar>
        </AppBar>
        <Grid container direction="row" justify="center">
          <Grid item xs={10}>
            <Grid container direction="column">
              <Grid item>
                <Dropzone onDrop={this.onDrop.bind(this)} multiple={false}>
                  <p>Drag a file here or click.</p>
                </Dropzone>
                {this.state.files.map(f => <li key={f.name}>{f.name}
                  - {f.size}
                  bytes</li>)
                }
              </Grid>
              <Grid item>
                <Button onClick={() => this.sendFile()} color="primary" variant="outlined" >
                  Legooooo
                </Button>
              </Grid>
              <Grid item>
                <DataTable courses={["COMP2041", "COMP9444", "COMP2121"]} />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    )
  }
}

export default withStyles(styles)(App)
