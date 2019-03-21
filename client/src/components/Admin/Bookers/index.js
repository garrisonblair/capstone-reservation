/* eslint-disable no-param-reassign */
import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';

import {
  Table, Segment, Pagination, Form, Button, Dropdown, Message, Icon,
} from 'semantic-ui-react';
import './Bookers.scss';
import api from '../../../utils/api';
import BookerRow from './BookerRow';
import BookerModal from './BookerModal';
import queryParams from '../../../utils/queryParams';


class Bookers extends Component {
  state = {
    bookers: [],
    isLoading: false,
    activePage: 1,
    totalPages: 0,
    dropdownOptions: [
      { text: 'Any', value: 'Any' },
      { text: 'Yes', value: true },
      { text: 'No', value: false }],
    valueActive: 'Any',
    valueSuperUser: 'Any',
    valueStaff: 'Any',
    valueSearch: '',
    valueSortTerm: '',
    searchLimit: 20,
    queriedUser: undefined,
  }

  componentDidMount() {
    // eslint-disable-next-line react/prop-types
    const { location } = this.props;
    const {
      searchLimit,
      valueSearch,
      valueActive,
      valueSuperUser,
      valueStaff,
      activePage,
      valueSortTerm,
    } = this.state;
    this.syncBookers(
      valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff, valueSortTerm,
    );

    const query = queryParams.parse(location.search);
    console.log(query);
    if (query.user) {
      api.getUser(query.user)
        .then((response) => {
          this.setState({ queriedUser: response.data });
        });
    }
  }

  getOffSet = (activePage, searchLimit) => (activePage * searchLimit) - searchLimit;

  syncBookers =
  (valueSearch, searchLimit, activePage, isActive, isSuperUser, isStaff, sortTerm) => {
    const offset = this.getOffSet(activePage, searchLimit);
    if (isActive === 'Any') {
      isActive = undefined;
    }
    if (isSuperUser === 'Any') {
      isSuperUser = undefined;
    }
    if (isStaff === 'Any') {
      isStaff = undefined;
    }
    if (sortTerm === '') {
      sortTerm = undefined;
    }
    this.setState({ isLoading: true });
    api.getUsers(valueSearch, searchLimit, offset, isActive, isSuperUser, isStaff, sortTerm)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({
            bookers: r.data.results,
            totalPages: Math.ceil(r.data.count / searchLimit),
          });
        }
      });
  }

  handlePaginationChange = (e, { activePage }) => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff,
    } = this.state;
    this.setState({ activePage });
    this.syncBookers(valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff);
  }

  handleSearchOnChange = (e, { value }) => { this.setState({ valueSearch: value }); }

  handleActiveOnChange = (e, { value }) => { this.setState({ valueActive: value }); }

  handleSuperUserOnChange = (e, { value }) => { this.setState({ valueSuperUser: value }); }

  handleStaffOnChange = (e, { value }) => { this.setState({ valueStaff: value }); }

  handleLimitOnChange = (e, { value }) => { this.setState({ searchLimit: value }); }

  handleUsernameSort = () => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff, activePage,
    } = this.state;
    let {
      valueSortTerm,
    } = this.state;

    if (valueSortTerm === 'username') {
      valueSortTerm = '-username';
    } else {
      valueSortTerm = 'username';
    }
    this.setState({ valueSortTerm });
    this.syncBookers(
      valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff, valueSortTerm,
    );
  }

  handleNameSort = () => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff, activePage,
    } = this.state;
    let {
      valueSortTerm,
    } = this.state;

    if (valueSortTerm === 'first_name') {
      valueSortTerm = '-first_name';
    } else {
      valueSortTerm = 'first_name';
    }
    this.setState({ valueSortTerm });
    this.syncBookers(
      valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff, valueSortTerm,
    );
  }

  handleEmailSort = () => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff, activePage,
    } = this.state;
    let {
      valueSortTerm,
    } = this.state;

    if (valueSortTerm === 'email') {
      valueSortTerm = '-email';
    } else {
      valueSortTerm = 'email';
    }
    this.setState({ valueSortTerm });
    this.syncBookers(
      valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff, valueSortTerm,
    );
  }

  handleSearchOnClick = () => {
    const {
      searchLimit, valueSearch, valueActive, valueSuperUser, valueStaff,
    } = this.state;
    this.setState({ activePage: 1 });
    this.syncBookers(valueSearch, searchLimit, 1, valueActive, valueSuperUser, valueStaff);
  }

  closeModal = () => {
    this.setState({ queriedUser: undefined });
  }

  handleResetOnClick = () => {
    const valueActive = 'Any';
    const valueSearch = '';
    const valueStaff = 'Any';
    const valueSuperUser = 'Any';
    const valueSortTerm = '';
    this.setState({
      valueActive,
      valueSearch,
      valueStaff,
      valueSuperUser,
      valueSortTerm,
    });
    const {
      searchLimit, activePage,
    } = this.state;
    this.syncBookers(
      valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff, valueSortTerm,
    );
  }

  render() {
    const {
      bookers, isLoading, activePage, totalPages,
      dropdownOptions, valueActive, valueSuperUser,
      valueStaff, valueSearch, searchLimit, valueSortTerm,
      queriedUser,
    } = this.state;
    return (
      <div id="bookers">
        <h1>Bookers</h1>
        <Form>
          <Form.Group widths="equal">
            <Form.Input fluid label="Search" icon="search" onChange={this.handleSearchOnChange} value={valueSearch} />
            <Form.Select fluid label="Super User" options={dropdownOptions} value={valueSuperUser} onChange={this.handleSuperUserOnChange} />
            <Form.Select fluid label="Active" options={dropdownOptions} value={valueActive} onChange={this.handleActiveOnChange} />
            <Form.Select fluid label="Staff" options={dropdownOptions} value={valueStaff} onChange={this.handleStaffOnChange} />
          </Form.Group>
          Table maximum size:
          <Dropdown
            className="table-max-size"
            options={[
              { text: 5, value: 5 },
              { text: 10, value: 10 },
              { text: 20, value: 20 },
              { text: 40, value: 40 },
            ]}
            selection
            compact
            value={searchLimit}
            onChange={this.handleLimitOnChange}
          />
          <br />
          <br />
          <Button color="blue" onClick={this.handleSearchOnClick}>
            Search
          </Button>
          <Button onClick={this.handleResetOnClick}>
            Reset
          </Button>
        </Form>
        <Segment loading={isLoading}>
          <Table>
            <Table.Header>
              <Table.Row key="-1">
                <Table.HeaderCell textAlign="center" className="sortable-button" onClick={this.handleUsernameSort}>
                  Username
                  {valueSortTerm === 'username' ? <Icon size="small" name="caret up" /> : null}
                  {valueSortTerm === '-username' ? <Icon size="small" name="caret down" /> : null}
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center" className="sortable-button" onClick={this.handleNameSort}>
                  Full name
                  {valueSortTerm === 'first_name' ? <Icon size="small" name="caret up" /> : null}
                  {valueSortTerm === '-first_name' ? <Icon size="small" name="caret down" /> : null}
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center" className="sortable-button" onClick={this.handleEmailSort}>
                  Email
                  {valueSortTerm === 'email' ? <Icon size="small" name="caret up" /> : null}
                  {valueSortTerm === '-email' ? <Icon size="small" name="caret down" /> : null}
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Super User
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Staff
                </Table.HeaderCell>
                <Table.HeaderCell textAlign="center">
                  Active
                </Table.HeaderCell>
                <Table.HeaderCell />
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {bookers.map(b => (
                <BookerRow
                  booker={b}
                  key={b.id}
                  syncBookers={() => this.syncBookers(
                    valueSearch, searchLimit, activePage, valueActive, valueSuperUser, valueStaff,
                  )
                  }
                />
              ))}
            </Table.Body>
          </Table>
          {bookers.length === 0 ? (
            <Message>
              <Message.Header>Empty list</Message.Header>
              <p>
                No bookers correspond to the specifications.
              </p>
            </Message>
          ) : null}
          {totalPages !== 0 ? (
            <Pagination
              activePage={activePage}
              totalPages={totalPages}
              onPageChange={this.handlePaginationChange}
            />
          ) : null}
        </Segment>
        { queriedUser ? <BookerModal show booker={queriedUser} onClose={this.closeModal} /> : null }
      </div>
    );
  }
}

export default withRouter(Bookers);
