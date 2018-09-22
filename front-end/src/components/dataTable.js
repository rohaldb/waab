import React, {Component} from 'react'
import { withStyles } from '@material-ui/core/styles'
import PropTypes from 'prop-types';
import _ from 'lodash'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const styles = theme => ({
  root: {
      width: '100%',
      marginTop: theme.spacing.unit * 3,
      overflowX: 'auto',
    },
    table: {
      minWidth: 400,
    },
    row: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.background.default,
      },
    },
})

class App extends Component {

  static propTypes = {
    courses: PropTypes.array.isRequired,
  }

  render() {
    const { classes, courses } = this.props

    if (_.size(courses) === 0) {
      return null
    }
    return (
      <Paper className={classes.root}>
      
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <CustomTableCell>Name</CustomTableCell>
            <CustomTableCell numeric>Code</CustomTableCell>
            <CustomTableCell numeric>Semester(s) Offered</CustomTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {_.map(courses, (x, i) => {
            return (
              <TableRow className={classes.row} key={i}>
                <CustomTableCell  style={{color: this.props.completed ? 'green' : 'red'}} component="th" scope="row">
                  {x}
                </CustomTableCell>
                <CustomTableCell >3</CustomTableCell>
                <CustomTableCell>3</CustomTableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Paper>
    )
  }
}

export default withStyles(styles)(App)
