import React, { Component } from 'react';
import {
  Table,
  Pagination,
  Icon,
  Dropdown,
  Input,
  Button,
  Segment,
  Grid,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import 'react-dates/initialize';
import { SingleDatePicker } from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import moment from 'moment';
import api from '../../../utils/api';
import BookingActivityModal from './BookingActivityModal';
import '../Admin.scss';
import UserSearch from '../../ReusableComponents/UserSearch';

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
    logsToDisplay: [],
    tableHeaders: ['date', 'type', 'action', 'user'],
    activePage: 1,
    logsPerPage: 10,
    totalLogCount: 0,
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
    isLoading: false,
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

  getLogs = () => {
    const {
      logsPerPage,
      activePage,
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

    this.setState({ isLoading: true });
    data.limit = logsPerPage;
    data.offset = logsPerPage * activePage - logsPerPage;
    api.getLogEntries(data)
      .then((response) => {
        this.setState({ isLoading: false });
        if (response.status === 200) {
          this.setState({
            logsToDisplay: response.data.results,
            totalLogCount: response.data.count,
          });
        }
      })
      .catch(() => {
        sweetAlert(':(', 'We are sorry. There was a problem getting the logs', 'error');
      });
  }

  handlePaginationChange = (e, { activePage }) => {
    this.setState({ activePage }, this.getLogs);
  }

  handlePaginationSettingsChange = (e, change) => {
    this.setState({ activePage: 1, logsPerPage: change.value }, this.getLogs);
  }

  showDetails = (log) => {
    this.setState({ selectedLog: log }, () => {
      this.setState({ showBookingActivityModal: true });
    });
  }

  handleSearchInput = (e, change) => {
    this.setState({ [change.name]: change.value !== '' ? change.value : null });
  }

  handleUserSelect = (user) => {
    if (user) {
      this.setState({ userId: user.id });
    } else {
      this.setState({ userId: null });
    }
  }

  handleOnUseObjectAsFilter = (contentType, id) => {
    this.handleSearchInput(null, { name: 'contentTypeId', value: contentType.id });
    this.handleSearchInput(null, { name: 'objectId', value: id });

    this.handleOnCloseBookingActivityModal();
  }

  handleOnCloseBookingActivityModal = () => {
    this.setState({ showBookingActivityModal: false, selectedLog: null });
  }

  handleSearch = () => {
    this.getLogs();
  }

  handleClear = () => {
    this.setState({
      from: null,
      to: null,
      contentTypeId: null,
      objectId: null,
      userId: null,
    });
    this.getLogs();
  }

  renderLogs = () => {
    const { logsToDisplay } = this.state;
    return (
      <Table.Body>
        {logsToDisplay.map(log => (
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
      tableHeaders,
      logsToDisplay,
      activePage,
      elementsPerPage,
      from,
      to,
      focusedFrom,
      focusedTo,
      contentTypes,
      contentTypeId,
      objectId,
      logsPerPage,
      totalLogCount,
    } = this.state;
    const totalPages = Math.ceil(totalLogCount / logsPerPage);

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
        <Grid>
          <Grid.Column largeScreen={5} mobile={16}>
            <Dropdown
              fluid
              placeholder="Type..."
              search
              selection
              options={contentTypesOptions}
              name="contentTypeId"
              value={contentTypeId == null ? '' : contentTypeId}
              onChange={this.handleSearchInput}
            />
          </Grid.Column>
          <Grid.Column largeScreen={5} mobile={16}>
            <Input
              fluid
              placeholder="Object ID..."
              name="objectId"
              value={objectId == null ? '' : objectId}
              onChange={this.handleSearchInput}
            />
          </Grid.Column>
          <Grid.Column largeScreen={6} mobile={16}>
            <UserSearch
              maxUsers={10}
              onSelect={this.handleUserSelect}
            />
          </Grid.Column>
        </Grid>
        <Button onClick={this.handleSearch}>Filter</Button>
        <Button onClick={this.handleClear}>Clear</Button>
        <Table celled fixed selectable>
          <Table.Header>
            <Table.Row>
              {tableHeaders.map(header => (
                <Table.HeaderCell
                  key={header}
                >
                  {header}
                </Table.HeaderCell>
              ))
              }
            </Table.Row>
          </Table.Header>

          {logsToDisplay.length > 0 ? this.renderLogs() : BookingActivity.renderEmptyLogs()}
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
    const { selectedLog, showBookingActivityModal, isLoading } = this.state;
    return (
      <div className="admin">
        <h1>Booking activity</h1>
        <Segment loading={isLoading}>
          {this.renderBookingActivity()}
          <BookingActivityModal
            log={selectedLog}
            show={showBookingActivityModal}
            onClose={this.handleOnCloseBookingActivityModal}
            onUseObjectAsFilter={this.handleOnUseObjectAsFilter}
          />
        </Segment>
      </div>
    );
  }
}

export default BookingActivity;
