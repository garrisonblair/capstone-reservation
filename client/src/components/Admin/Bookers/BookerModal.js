import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Modal, Dropdown, Button, List, Icon,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './BookerModal.scss';

class BookerModal extends Component {
  state = {
    myPrivileges: [],
    dropdownOptions: [],
    privilegeValue: '',
    privileges: [],
  }

  componentDidMount() {
    const { booker } = this.props;
    const { dropdownOptions } = this.state;
    this.setState({ myPrivileges: booker.booker_profile.privilege_categories });
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

  handleRemovePrivilege = (privilege) => {
    const { myPrivileges } = this.state;
    const { booker } = this.props;
    api.removePrivilege([booker.id], privilege.id)
      .then(() => {
        // sweetAlert('Completed',
        //   'Privilege was removed.',
        //   'success');
      });
    this.setState({ myPrivileges: myPrivileges.filter(p => p !== privilege) });
  }

  handleAddPrivilegeClick = () => {
    const { privilegeValue, privileges, myPrivileges } = this.state;
    const { booker } = this.props;
    if (myPrivileges.some(p => p.id === privilegeValue)) {
      sweetAlert('Warning', 'You already have that privilege', 'warning');
      return;
    }
    api.addPrivilege([booker.id], privilegeValue)
      .then((r) => {
        if (r.status === 200) {
          const privilege = privileges.find(p => p.id === privilegeValue);
          myPrivileges.push(privilege);
          this.setState({ myPrivileges });
        }
      });
  }

  renderPrivilegeRow = privilege => (
    <List.Item key={privilege.id}>
      <List.Content floated="right">
        <Button onClick={() => this.handleRemovePrivilege(privilege)}>Remove</Button>
      </List.Content>
      <List.Content className="privilege-name">
        <Icon name="circle" />
        {privilege.name}
      </List.Content>
    </List.Item>
  )

  render() {
    const { show, booker, onClose } = this.props;
    const { dropdownOptions, myPrivileges } = this.state;
    return (
      <Modal open={show} onClose={onClose} size="small" id="booker-modal">
        <Modal.Header>
          Booker details (
          {booker.username}
          )
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h3>Full name:</h3>
            {`${booker.last_name}, ${booker.first_name}`}
            <h3>Email</h3>
            {booker.email.length !== 0 ? booker.email : '[Empty]'}
            <h3>Privileges</h3>
            <div className="privilege-section">
              <List divided className="booker-list">
                {myPrivileges.map(
                  p => this.renderPrivilegeRow(p),
                )}
              </List>
              <Dropdown
                placeholder="Privilege to add"
                selection
                onChange={this.handleDropdownChange}
                options={dropdownOptions}
              />
              <Button onClick={this.handleAddPrivilegeClick} color="blue">Add Privilege</Button>
            </div>
          </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={onClose}>Close</Button>
        </Modal.Actions>
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
