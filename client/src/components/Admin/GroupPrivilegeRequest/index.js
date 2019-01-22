import React, { Component } from 'react';
import { Table, Dropdown, Message } from 'semantic-ui-react';
import api from '../../../utils/api';
import PrivilegeRequestRow from './PrivilegeRequestRow';
import './GroupPrivilegeRequest.scss';


class GroupPrivilegeRequest extends Component {
  state = {
    requests: [],
    filterBy: '',
    activeAll: true,
    activePending: false,
    activeApproved: false,
    activeDeny: false,
  }

  componentDidMount() {
    this.syncPrivileges();
  }

  syncPrivileges = () => {
    api.getPrivilegeRequests()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ requests: r.data });
        }
      });
  }

  noFilter = () => {
    this.setState({
      activeAll: true,
      activeApproved: false,
      activeDeny: false,
      activePending: false,
      filterBy: '',
    });
  }

  filterByPending = () => {
    this.setState({
      activeAll: false,
      activeApproved: false,
      activeDeny: false,
      activePending: true,
      filterBy: 'Pending',
    });
  }

  filterByApproved = () => {
    this.setState({
      activeAll: false,
      activeApproved: true,
      activeDeny: false,
      activePending: false,
      filterBy: 'Approved',
    });
  }

  filterByDenied = () => {
    this.setState({
      activeAll: false,
      activeApproved: false,
      activeDeny: true,
      activePending: false,
      filterBy: 'Denied',
    });
  }

  renderDropDown = () => {
    const {
      activeAll, activeApproved, activeDeny, activePending,
    } = this.state;
    return (
      <Dropdown
        text="Filter"
        icon="filter"
        floating
        labeled
        button
        value="suu"
        className="icon"
      >
        <Dropdown.Menu>
          <Dropdown.Header icon="tags" content="Filter by status" />
          <Dropdown.Item onClick={this.noFilter} active={activeAll}>
            Show All
          </Dropdown.Item>
          <Dropdown.Item onClick={this.filterByPending} active={activePending}>
            Pending
          </Dropdown.Item>
          <Dropdown.Item onClick={this.filterByApproved} active={activeApproved}>
            Approved
          </Dropdown.Item>
          <Dropdown.Item onClick={this.filterByDenied} active={activeDeny}>
            Denied
          </Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
    );
  }

  renderTable = requests => (
    <Table>
      <Table.Header>
        <Table.Row key="1">
          <Table.HeaderCell>
            Group&lsquo;s name
          </Table.HeaderCell>
          <Table.HeaderCell>
            Requested Privilege
          </Table.HeaderCell>
          <Table.HeaderCell>
            Status
          </Table.HeaderCell>
          {/* This tab is for buttons */}
          <Table.HeaderCell />
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {requests.map(
          r => <PrivilegeRequestRow request={r} key={r.id} syncMethod={this.syncPrivileges} />,
        )}
      </Table.Body>
    </Table>
  )

  render() {
    const { filterBy } = this.state;
    let { requests } = this.state;
    if (filterBy.length > 0) {
      requests = requests.filter(r => r.status === filterBy);
    }
    return (
      <div id="group-privilege-request">
        <h2>Group&lsquo;s Privilege Request</h2>
        {this.renderDropDown()}
        {requests.length === 0 ? (
          <Message>
            <p>
              There is no request
              {filterBy.length > 0 ? ` with filter '${filterBy}'` : null}
            </p>
          </Message>
        ) : this.renderTable(requests)}

      </div>
    );
  }
}

export default GroupPrivilegeRequest;
