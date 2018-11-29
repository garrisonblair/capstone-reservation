import _ from 'lodash';
import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';

class BookingActivity extends Component {
  static formatAction(flag) {
    if (flag === 1) {
      return 'Create';
    }
    if (flag === 2) {
      return 'Edit';
    }
    if (flag === 3) {
      return 'Delete';
    }
    return '';
  }

  static formatDate(d) {
    const date = d.split('T');
    const time = date[1].split('.');
    return `${date[0]}\n${time[0]}`;
  }

  state = {
    column: null,
    direction: null,
    logs: [],
    tableHeaders: ['date', 'type', 'action', 'user'],
  }

  componentDidMount() {
    api.getLogEntries()
      .then((response) => {
        if (response.status === 200) {
          this.setState({ logs: response.data });
        }
      })
      .catch(() => {
        sweetAlert(':(', 'We are sorry. There was a problem getting the logs', 'error');
      });
  }

  handleSort = clickedColumn => () => {
    const { column, logs, direction } = this.state;
    if (column !== clickedColumn) {
      this.setState({
        column: clickedColumn,
        logs: _.sortBy(logs, [clickedColumn]),
        direction: 'ascending',
      });

      return;
    }

    this.setState({
      logs: logs.reverse(),
      direction: direction === 'ascending' ? 'descending' : 'ascending',
    });
  }

  showDetails = (log) => {
    let logObject = log.object_repr;
    logObject = logObject.replace(/,/g, '<br>');
    console.log(log)
    sweetAlert(
      'Details',
      `${BookingActivity.formatDate(log.action_time)}
      <br>${BookingActivity.formatAction(log.action_flag)} ${log.content_type.app_label}
      <br>by ${log.user}
      <br>${logObject}`,
    );
  }

  renderBookingActivity = () => {
    const {
      column,
      direction,
      tableHeaders,
      logs,
    } = this.state;

    return (
      <Table sortable celled fixed selectable inverted>
        <Table.Header>
          <Table.Row>
            { tableHeaders.map(header => (
              <Table.HeaderCell
                sorted={column === header ? direction : null}
                onClick={this.handleSort(header)}
                key={header}
              >
                {header}
              </Table.HeaderCell>
            ))
            }
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {logs.map(log => (
            <Table.Row key={log.id} onClick={() => this.showDetails(log)}>
              <Table.Cell>
                {BookingActivity.formatDate(log.action_time)}
              </Table.Cell>
              <Table.Cell>{log.content_type.app_label}</Table.Cell>
              <Table.Cell>
                {BookingActivity.formatAction(log.action_flag)}
              </Table.Cell>
              <Table.Cell>{log.user}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    );
  }

  render() {
    return (
      <div className="admin">
        <h1>Booking activity</h1>
        { this.renderBookingActivity() }
      </div>
    );
  }
}

export default BookingActivity;
