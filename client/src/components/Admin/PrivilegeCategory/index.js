import React, {Component} from 'react';
import {Button, Icon, Table, TableCell} from 'semantic-ui-react';
import api from '../../../utils/api';
import AdminRequired from '../../HOC/AdminRequired';
import AddPrivilegeModal from './AddPrivilegeModal';
import PrivilegeDetailsModal from './PrivilegeDetailsModal';
import '../Admin.scss';


// TODO: Pagination
class PrivilegeCategory extends Component {

  state = {
    privileges: [],
    privilege: {},
    showAddPrivilegeModal: false,
    showAssignPrivilegeModal: false,
    showDetailsModal: false
  }

  getPrivileges = () => {
    if(this.props.privilegesMock) {
      this.setState({privileges: this.props.privilegesMock})
      return;
    }
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

  handleDisplayPrivilege = (privilege) => {
    this.setState({
      showDetailsModal: true,
      privilege
    })
  }

  handleOnCloseAddPrivilegeModal = () => {
    this.getPrivileges();
    this.setState({
      showAddPrivilegeModal: false
    })
  }

  handleOnCloseDisplayPrivilegeModal = () => {
    this.setState({
      showDetailsModal: false,
      privilege: {}
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
      'Booking Start Time',
      'Booking End Time',
      ''
    ]

    let body = privileges.map((privilege) =>
      <Table.Row key={privilege.id}>
        <Table.Cell>{privilege.name}</Table.Cell>
        <Table.Cell>{privilege.parent_category || '-'}</Table.Cell>
        <Table.Cell>{privilege.booking_start_time}</Table.Cell>
        <Table.Cell>{privilege.booking_end_time}</Table.Cell>
        <TableCell>
          <Button
            icon
            primary
            size='small'
            onClick={() => this.handleDisplayPrivilege(privilege)}
          >
            <Icon name='eye'/>
          </Button>
        </TableCell>
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
    const {privilege, privileges, showAddPrivilegeModal, showDetailsModal} = this.state;
    return (
      <div className="privileges">
        <h1>Privileges</h1>
        {this.renderControls()}
        {this.renderTable()}
        <AddPrivilegeModal
          privileges={privileges}
          show={showAddPrivilegeModal}
          onClose={this.handleOnCloseAddPrivilegeModal}
        />
        <PrivilegeDetailsModal
          privilege={privilege}
          show={showDetailsModal}
          onClose={this.handleOnCloseDisplayPrivilegeModal}
        />
      </div>
    )
  }
}

export default AdminRequired(PrivilegeCategory);
