import _ from 'lodash';
import React, { Component } from 'react';
import SideNav from '../SideNav';
import { Table } from 'semantic-ui-react';

const tableData = [
  { id: 1, time: '10:00', type: 'booking create', user: '1' },
  { id: 2, time: '12:00', type: 'booking create', user: '2' },
  { id: 3, time: '15:00', type: 'booking delete', user: '3' },
  { id: 4, time: '20:00', type: 'booking edit', user: '2' },
]

class BookingActivity extends Component {
  state = {
    column: null,
    data: tableData,
    direction: null,
  }

  handleSort = clickedColumn => () => {
    const { column, data, direction } = this.state

    if (column !== clickedColumn) {
      this.setState({
        column: clickedColumn,
        data: _.sortBy(data, [clickedColumn]),
        direction: 'ascending',
      })

      return
    }

    this.setState({
      data: data.reverse(),
      direction: direction === 'ascending' ? 'descending' : 'ascending',
    })
  }

  renderBookingActivity = () => {
    const { column, data, direction } = this.state;
    return (
      <Table sortable celled fixed>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell
              sorted={column === 'time' ? direction : null}
              onClick={this.handleSort('time')}
            >
              Time
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'type' ? direction : null}
              onClick={this.handleSort('type')}
            >
              Type
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'user' ? direction : null}
              onClick={this.handleSort('user')}
            >
              User
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {_.map(data, ({ id, time, type, user }) => (
            <Table.Row key={id}>
              <Table.Cell>{time}</Table.Cell>
              <Table.Cell>{type}</Table.Cell>
              <Table.Cell>{user}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    )
  }

  render() {
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'stats'} />
          <div className="admin__content">
            <div id="booking-activity">
              <h1>Booking activity</h1>
              { this.renderBookingActivity() }
            </div>
          </div>
        </div>
      </div>
      
    )
  }
}

export default BookingActivity;