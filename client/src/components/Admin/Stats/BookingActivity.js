import _ from 'lodash';
import cloneDeep from 'lodash/cloneDeep';
import React, { Component } from 'react';
import {
  Table,
  Pagination,
  Icon,
  Dropdown,
  Input,
} from 'semantic-ui-react';
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
    logsToDisplay: [],
    tableHeaders: ['date', 'type', 'action', 'user'],
    activePage: 1,
    logsPerPage: 10,
    elementsPerPage: [
      { text: '5', value: 5 },
      { text: '10', value: 10 },
      { text: '20', value: 20 },
      { text: '30', value: 30 },
      { text: '40', value: 40 },
      { text: '50', value: 50 },
    ],
    from: null,
    to: null,
    contentTypeId: null,
    objectId: null,
    userId: null,
  }

  componentDidMount() {
    this.getLogs();
  }

  getLogs = (data) => {
    api.getLogEntries(data)
      .then((response) => {
        if (response.status === 200) {
          console.log(response.data);
          const logsToDisplay = this.setLogsToDisplay(response.data);
          this.setState({ logs: response.data, logsToDisplay });
        }
      })
      .catch(() => {
        sweetAlert(':(', 'We are sorry. There was a problem getting the logs', 'error');
      });
  }

  setLogsToDisplay(data) {
    const { logsPerPage } = this.state;
    const logs = cloneDeep(data);
    const logsToDisplay = [];
    while (logs.length) {
      logsToDisplay.push(logs.splice(0, logsPerPage));
    }
    return logsToDisplay;
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
    }, () => {
      this.setState({ logsToDisplay: this.setLogsToDisplay(logs) });
    });
  }

  handlePaginationChange = (e, { activePage }) => this.setState({ activePage });

  handlePaginationSettingsChange = (e, change) => {
    const { logs } = this.state;
    this.setState({ activePage: 1, logsPerPage: change.value }, () => {
      this.setState({ logsToDisplay: this.setLogsToDisplay(logs) });
    });
  }

  showDetails = (log) => {
    let logObject = log.object_repr;
    logObject = logObject.replace(/,/g, '<br>');
    sweetAlert(
      'Details',
      `${BookingActivity.formatDate(log.action_time)}
      <br>${BookingActivity.formatAction(log.action_flag)} ${log.content_type.app_label}
      <br>by ${log.user}
      <br>${logObject}`,
    );
  }

  handleSearchInput = (e, change) => {
    this.setState({ [change.name]: change.value });
  }

  handleSearch = () => {
    const {
      from,
      to,
      contentTypeId,
      objectId,
      userId,
    } = this.state;

    const data = {
      from,
      to,
      content_type_id: contentTypeId,
      object_id: objectId,
      user_id: userId,
    };
    this.getLogs(data);
  }

  renderLogs = () => {
    const { logsToDisplay, activePage } = this.state;
    return (
      <Table.Body>
        {logsToDisplay[activePage - 1].map(log => (
          <Table.Row key={log.id} onClick={() => this.showDetails(log)}>
            <Table.Cell>
              {BookingActivity.formatDate(log.action_time)}
            </Table.Cell>
            <Table.Cell>{log.content_type.app_label}</Table.Cell>
            <Table.Cell>
              {BookingActivity.formatAction(log.action_flag)}
            </Table.Cell>
            <Table.Cell>{log.user.username}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    );
  }

  static renderEmptyLogs() {
    return (
      <Table.Body>
        <Table.Row>
          <Table.Cell>
            No logs found
          </Table.Cell>
        </Table.Row>
      </Table.Body>
    );
  }

  renderBookingActivity = () => {
    const {
      column,
      direction,
      tableHeaders,
      logsToDisplay,
      activePage,
      elementsPerPage,
    } = this.state;
    const totalPages = logsToDisplay.length;

    return (
      <div>
        <Pagination
          activePage={activePage}
          ellipsisItem={{ content: <Icon name="ellipsis horizontal" />, icon: true }}
          firstItem={{ content: <Icon name="angle double left" />, icon: true }}
          lastItem={{ content: <Icon name="angle double right" />, icon: true }}
          prevItem={{ content: <Icon name="angle left" />, icon: true }}
          nextItem={{ content: <Icon name="angle right" />, icon: true }}
          totalPages={totalPages}
          onPageChange={this.handlePaginationChange}
        />

        <Dropdown placeholder="# logs" search selection options={elementsPerPage} onChange={this.handlePaginationSettingsChange} />

        <Input icon={<Icon name="search" inverted circular link onClick={this.handleSearch} />} placeholder="Type..." name="contentTypeId" onChange={this.handleSearchInput} />

        <Table sortable celled fixed selectable>
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

          { logsToDisplay.length > 0 ? this.renderLogs() : BookingActivity.renderEmptyLogs() }
        </Table>
      </div>
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
