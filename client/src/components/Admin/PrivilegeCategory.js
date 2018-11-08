import React, {Component} from 'react';
import {Button, Icon, Table} from 'semantic-ui-react';
import api from '../../utils/api';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import AddPrivilegeModal from './AddPrivilegeModal';
import './Admin.scss';


// TODO: Pagination
class PrivilegeCategory extends Component {

  state = {
    privileges: [],
    showAddPrivilegeModal: false,
    showAssignPrivilegeModal: false
  }

  getPrivileges = () => {
    api.getPrivileges()
    .then((response) => response.data)
    .then((privileges) => {
      this.setState({
        privileges
      })
    })
    .catch((error) => {
      console.log(error);
    })
  }

  handleAddPrivilege = () => {
    this.setState({
      showAddPrivilegeModal: true
    })
  }

  handleOnCloseAdPrivilegeModal = () => {
    this.getPrivileges();
    this.setState({
      showAddPrivilegeModal: false
    })
  }

  renderControls() {
    return (
      <div>
        <Button icon labelPosition='left' primary size='small' onClick={this.handleAddPrivilege}>
          <Icon name='plus'/> Add
        </Button>
        <Button icon labelPosition='left' primary size='small'>
          <Icon name='plus'/> Assign
        </Button>
      </div>
    )
  }

  renderTable() {
    const {privileges} = this.state;
    let headers = [
      'Name',
      'Parent Category',
      'Max Days Until Booking',
      'Max Bookings',
      'Recurring Booking Permission',
      'Max Recurring Bookings',
      'Booking Valid Time'
    ]

    let body = privileges.map((privilege) =>
      <Table.Row key={privilege.id}>
        <Table.Cell>{privilege.name}</Table.Cell>
        <Table.Cell>{privilege.parent_category || '-'}</Table.Cell>
        <Table.Cell>{privilege.max_days_until_booking}</Table.Cell>
        <Table.Cell>{privilege.max_bookings}</Table.Cell>
        <Table.Cell>
          <Icon
            name={privilege.can_make_recurring_booking? 'check circle': 'times circle'}
            color={privilege.can_make_recurring_booking? 'green': 'red'}
          />
        </Table.Cell>
        <Table.Cell>{privilege.max_recurring_bookings}</Table.Cell>
        <Table.Cell>{`${privilege.booking_start_time} - ${privilege.booking_end_time}`}</Table.Cell>
      </Table.Row>
    )

    let table = (
      <Table celled>
        <Table.Header>
          <Table.Row>
            {
              headers.map((header, index) =>
                <Table.HeaderCell key={index}>
                  {header}
                </Table.HeaderCell>
              )
            }
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {body}
        </Table.Body>
      </Table>
    )
    return table;
  }

  componentDidMount() {
    this.getPrivileges();
  }

  render() {
    const {privileges, showAddPrivilegeModal} = this.state;
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'privileges'}/>
          <div className="admin__content">
            <h1>Privileges</h1>
            {this.renderControls()}
            {this.renderTable()}
            <AddPrivilegeModal
              privileges={privileges}
              show={showAddPrivilegeModal}
              onClose={this.handleOnCloseAdPrivilegeModal}
            />
          </div>
        </div>
      </div>
    )
  }
}

export default AdminRequired(PrivilegeCategory);
