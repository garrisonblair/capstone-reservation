import React, { Component } from 'react';
import {
  Button,
  Icon,
  Table,
  TableCell,
  Segment,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
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
    showDetailsModal: false,
    isLoading: false,
  }

  componentDidMount() {
    this.getPrivileges();
  }

  getPrivileges = () => {
    this.setState({ isLoading: true });
    // eslint-disable-next-line react/prop-types
    const { privilegesMock } = this.props;
    if (privilegesMock) {
      this.setState({ privileges: privilegesMock });
      return;
    }
    api.getPrivileges()
      .then(response => response.data)
      .then((privileges) => {
        this.setState({ isLoading: false });
        this.setState({
          privileges,
        });
      });
  }

  handleAddPrivilege = () => {
    this.setState({
      showAddPrivilegeModal: true,
    });
  }

  handleAssignAllPrivileges = () => {
    sweetAlert.fire({
      title: 'Assign Privileges to all users?',
      text: 'This will assign privileges to users based on which courses they are taking',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, assign privileges!',
    }).then((result) => {
      if (result.value) {
        api.assignAllPrivileges()
          .then(
            sweetAlert.fire({
              position: 'top',
              type: 'success',
              title: 'Completed',
              text: 'Privieges successfully assigned',
            }),
          );
      }
    });
  }

  handleDisplayPrivilege = (privilege) => {
    this.setState({
      showDetailsModal: true,
      privilege,
    });
  }

  handleOnCloseAddPrivilegeModal = () => {
    this.getPrivileges();
    this.setState({
      showAddPrivilegeModal: false,
    });
  }

  handleOnCloseDisplayPrivilegeModal = () => {
    this.setState({
      showDetailsModal: false,
      privilege: {},
    });
  }

  renderControls() {
    return (
      <div>
        <Button icon labelPosition="left" primary size="small" onClick={this.handleAddPrivilege}>
          <Icon name="plus" />
          Add
        </Button>
        <Button icon labelPosition="left" primary size="small" onClick={this.handleAssignAllPrivileges}>
          <Icon name="upload" />
          Assign All
        </Button>
      </div>
    );
  }

  renderTable() {
    const { privileges } = this.state;
    const headers = [
      'Name',
      'Parent Category',
      'Related Course',
      '',
    ];

    const body = privileges.map(privilege => (
      <Table.Row key={privilege.id}>
        <Table.Cell>{privilege.name}</Table.Cell>
        <Table.Cell>{privilege.parent_category ? privilege.parent_category.name : '-'}</Table.Cell>
        <Table.Cell>{privilege.related_course || '-'}</Table.Cell>
        <TableCell>
          <Button
            icon
            primary
            size="small"
            onClick={() => this.handleDisplayPrivilege(privilege)}
          >
            <Icon name="eye" />
          </Button>
        </TableCell>
      </Table.Row>
    ));

    const table = (
      <Table celled>
        <Table.Header>
          <Table.Row>
            {
              headers.map((header, index) => (
                // eslint-disable-next-line react/no-array-index-key
                <Table.HeaderCell key={index}>
                  {header}
                </Table.HeaderCell>
              ))
            }
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {body}
        </Table.Body>
      </Table>
    );
    return table;
  }

  render() {
    const
      {
        privilege,
        privileges,
        showAddPrivilegeModal,
        showDetailsModal,
        isLoading,
      } = this.state;
    return (
      <div className="privileges">
        <h1>Privileges</h1>
        <Segment loading={isLoading}>
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
        </Segment>
      </div>
    );
  }
}

export default AdminRequired(PrivilegeCategory);
