import _ from 'lodash';
import cloneDeep from 'lodash/cloneDeep';
import React, { Component } from 'react';
import {
  Table,
  Pagination,
  Icon,
  Dropdown,
  Input,
  Button,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import 'react-dates/initialize';
import { SingleDatePicker } from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import moment from 'moment';
import api from '../../../utils/api';
import BookingActivityModal from './BookingActivityModal';
import '../Admin.scss';

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
    showBookingActivityModal: false,
    selectedLog: null,
    focusedFrom: false,
    focusedTo: false,
    contentTypes: [],
  }

  componentDidMount() {
    this.getLogs();
    api.getContentTypes()
      .then((response) => {
        if (response.status === 200) {
          this.setState({ contentTypes: response.data });
        }
      });
  }

  getLogs = (data) => {
    api.getLogEntries(data)
      .then((response) => {
        if (response.status === 200) {
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
    this.setState({ selectedLog: log }, () => {
      this.setState({ showBookingActivityModal: true });
    });
  }

  handleSearchInput = (e, change) => {
    this.setState({ [change.name]: change.value !== '' ? change.value : null });
  }

  // handleContentTypeSearch = (e, change) => {
  //   this.setState({ })
  //   api.getLogEntries(data)
  //     .then((response) => {
  //       if (response.status === 200) {
  //         console.log(response.data);
  //         const logsToDisplay = this.setLogsToDisplay(response.data);
  //         this.setState({ logs: response.data, logsToDisplay });
  //       }
  //     })
  //     .catch(() => {
  //       sweetAlert(':(', 'We are sorry. There was a problem getting the logs', 'error');
  //     });
  // }

  handleOnCloseBookingActivityModal = () => {
    this.setState({ showBookingActivityModal: false, selectedLog: null });
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
      from: from == null ? null : moment(from).format('DD-MM-YYYY 00:59:59'),
      to: to == null ? null : moment(to).format('DD-MM-YYYY 23:59:59'),
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
            <Table.Cell>{log.content_type.model}</Table.Cell>
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
      from,
      to,
      focusedFrom,
      focusedTo,
      contentTypes,
    } = this.state;
    const totalPages = logsToDisplay.length;

    const contentTypesOptions = [];
    contentTypes.forEach((c) => {
      let text = c.model.charAt(0).toUpperCase() + c.model.slice(1);
      if (text === 'Recurringbooking') {
        text = 'Recurring booking';
      }
      contentTypesOptions.push({ text, value: c.id });
    });

    return (
      <div>
        <div>
          <SingleDatePicker
            isOutsideRange={() => false}
            numberOfMonths={1}
            date={from}
            onDateChange={date => this.setState({ from: date })}
            focused={focusedFrom}
            onFocusChange={({ focused }) => this.setState({ focusedFrom: focused })}
            id="from"
            placeholder="From"
          />
          <SingleDatePicker
            isOutsideRange={() => false}
            numberOfMonths={1}
            date={to}
            onDateChange={date => this.setState({ to: date })}
            focused={focusedTo}
            onFocusChange={({ focused }) => this.setState({ focusedTo: focused })}
            id="to"
            placeholder="To"
          />
        </div>
        <Dropdown placeholder="Type..." fluid search selection options={contentTypesOptions} name="contentTypeId" onChange={this.handleSearchInput} />
        <Input placeholder="Object ID..." name="objectId" onChange={this.handleSearchInput} />
        <Input placeholder="User..." name="userId" onChange={this.handleSearchInput} />
        <Button onClick={this.handleSearch}>Filter</Button>
        <Table sortable celled fixed selectable>
          <Table.Header>
            <Table.Row>
              { tableHeaders.map(header => (
                <Table.HeaderCell
                  sorted={column === header ? direction : null}
                  onClick={header === 'date' ? this.handleSort(header) : null}
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
        <Dropdown placeholder="# logs" search selection options={elementsPerPage} onChange={this.handlePaginationSettingsChange} />
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
      </div>
    );
  }

  render() {
    const { selectedLog, showBookingActivityModal } = this.state;
    return (
      <div className="admin">
        <h1>Booking activity</h1>
        { this.renderBookingActivity() }
        <BookingActivityModal
          log={selectedLog}
          show={showBookingActivityModal}
          onClose={this.handleOnCloseBookingActivityModal}
        />
      </div>
    );
  }
}

export default BookingActivity;
