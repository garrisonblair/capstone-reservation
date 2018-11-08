import React, {Component} from 'react';
import {Icon, Label, Menu, Table} from 'semantic-ui-react'
import api from '../../utils/api';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import './Admin.scss';


class PrivilegeCategory extends Component {

  state = {
    privileges: []
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

  renderTable() {
    const {privileges} = this.state;
    let headers = [
      'Name',
      'Parent',
      'Max Days Until Booking',
      'Max Bookings',
      'Can Make Recurring Booking',
      'Max Recurring Bookings',
      'Booking Start Time',
      'Booking End Time'
    ]

    let body = privileges.map((privilege) => {
      console.log(privilege);
      return (
        <Table.Row key={privilege.id}>
          <Table.Cell>{privilege.name}</Table.Cell>
          <Table.Cell>{privilege.parent_category || '-'}</Table.Cell>
          <Table.Cell>{privilege.max_days_until_booking}</Table.Cell>
          <Table.Cell>{privilege.max_bookings}</Table.Cell>
          <Table.Cell>{privilege.can_make_recurring_booking? 'Yes':'No'}</Table.Cell>
          <Table.Cell>{privilege.max_recurring_bookings}</Table.Cell>
          <Table.Cell>{privilege.booking_start_time}</Table.Cell>
          <Table.Cell>{privilege.booking_end_time}</Table.Cell>
        </Table.Row>
      )
    })

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
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'privileges'}/>
          <div className="admin__content">
            <div>Privileges</div>
            {this.renderTable()}
          </div>
        </div>
      </div>
    )
  }
}

export default AdminRequired(PrivilegeCategory);
