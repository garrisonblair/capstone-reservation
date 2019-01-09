import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Dropdown, Button, List,
} from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import PrivilegeRow from './PrivilegeRow';

class BookerModal extends Component {
  state = {
    // eslint-disable-next-line react/destructuring-assignment
    myPrivileges: [],
    dropdownOptions: [],
    privilegeValue: '',
    privileges: [],
  }

  componentDidMount() {
    const { booker } = this.props;
    const { dropdownOptions } = this.state;
    this.setState({ myPrivileges: booker.privilege_categories });
    api.getPrivileges()
      .then((result) => {
        this.setState({ privileges: result.data });
        result.data.map(
          // eslint-disable-next-line array-callback-return
          (p) => {
            dropdownOptions.push({ text: p.name, value: p.id, key: p.id });
            this.setState({ dropdownOptions });
          },
        );
      });
  }

  handleDropdownChange = (e, { value }) => {
    this.setState({ privilegeValue: value });
  }

  handleAddPrivilegeClick = () => {
    const { privilegeValue, privileges, myPrivileges } = this.state;
    const { booker } = this.props;
    api.addPrivilege([booker.user.username], privilegeValue)
      .then((r) => {
        if (r.status === 200) {
          const privilege = privileges.find(p => p.id === privilegeValue);
          myPrivileges.push(privilege);
          this.setState({ myPrivileges });
        }
      });
  }

  render() {
    const { show, booker, onClose } = this.props;
    const { dropdownOptions, myPrivileges } = this.state;
    return (
      <Modal open={show} onClose={onClose} size="small">
        <Modal.Header>
          Booker details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h4>Username:</h4>
            {booker.user.username}
            <h4>Privileges</h4>
            <Dropdown
              placeholder="Privilege"
              selection
              onChange={this.handleDropdownChange}
              options={dropdownOptions}
            />
            <Button onClick={this.handleAddPrivilegeClick}>Add Privilege</Button>
            <List>
              {myPrivileges.map(
                p => <PrivilegeRow divided privilege={p} key={p.id} />,
              )}
            </List>
          </Modal.Description>
        </Modal.Content>
      </Modal>
    );
  }
}

BookerModal.propTypes = {
  show: PropTypes.bool.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  booker: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default BookerModal;
