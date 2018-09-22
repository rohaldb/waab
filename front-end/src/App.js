import React, {Component} from 'react'
import CircularProgress from '@material-ui/core/CircularProgress';
import Dropzone from 'react-dropzone'
import Grid from '@material-ui/core/Grid'
import {withStyles} from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'
import {DataTable} from './components'
import _ from 'lodash'

const styles = theme => ({
  progress: {
    margin: theme.spacing.unit * 2,
    color: theme.palette.common.black
  },
  black: {
    backgroundColor: theme.palette.common.black
  }
})

class App extends Component {
  state = {
    files: [],
    completedCourses: null,
    alreadyCompleted: null,
    loading: false
  }

  onDrop(files) {
    this.setState({
      files
    }, () => this.sendFile())
  }

  sendFile = () => {
    var data = new FormData()
    data.append('file', this.state.files[0])

    this.setState({loading: true})

    fetch('http://localhost:5000/', { // Your POST endpoint
      method: 'POST',
      body: data,
      mode: 'cors'
    }).then(response => {
      console.log(response);
      return response.json()
    }).then(data => {
      console.log(data);
      this.setState({alreadyCompleted: data[0], completedCourses: data[1], loading: false})
    }).catch(error => {
      this.setState({loading: false})
      console.error(error)
    })
  }

  render() {
    const {classes} = this.props
    const {completedCourses, loading, alreadyCompleted} = this.state

    return (
      <div className='App'>
        <AppBar position="static">
          <Toolbar className={classes.black}>
            <Typography variant="title" color="inherit" className={classes.grow}>
              WAAB
            </Typography>
          </Toolbar>
        </AppBar>
        <Grid container direction="row" justify="center">
          <Grid item xs={10}>
            <Grid container direction="column" style={{
              textAlign: 'center'
            }}>
              <Grid item xs={5}>
                <Dropzone onDrop={this.onDrop.bind(this)} multiple={false}>
                  <p>Drag a file here or click.</p>
                </Dropzone>
              </Grid>
              <Grid item>
                <Grid container direction="row" justify="center" spacing={40}>
                  {loading
                    ? <CircularProgress className={classes.progress} size={50}/>
                    : null}
                  <Grid item xs={5}>
                    {_.isEmpty(completedCourses)
                      ? null
                      : (
                        <div>
                          <Typography variant="title">
                            Completed Courses
                          </Typography>
                          <DataTable courses={completedCourses} completed={true}/>  
                        </div>
                      )
                    }
                  </Grid>
                  <Grid item xs={5}>
                    
                    {_.isEmpty(alreadyCompleted)
                      ? null
                      : (
                        <div>
                          <Typography variant="title">
                            Remaining
                          </Typography>
                          <DataTable courses={alreadyCompleted}  completed={false}/>
                        </div>
                      )
}
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    )
  }
}

export default withStyles(styles)(App)
