import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Modal, Dropdown, Button } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';

class BookerModal extends Component {
  state = {
    privileges: [],
    privilegeValue: '',
  }

  componentDidMount() {
    const { privileges } = this.state;
    api.getPrivileges()
      .then((result) => {
        result.data.map(
          // eslint-disable-next-line array-callback-return
          (p) => {
            privileges.push({ text: p.name, value: p.id, key: p.id });
            this.setState({ privileges });
          },
        );
      });
  }

  handleDropdownChange = (e, { value }) => {
    this.setState({ privilegeValue: value });
  }

  handleAddPrivilegeClick = () => {
    const { privilegeValue } = this.state;
    const { booker } = this.props;
    console.log(booker.username);
    console.log(privilegeValue);
    api.addPrivilege([booker.username], privilegeValue)
      .then((r) => {
        if (r.status !== 200) {
          console.log(r);
        }
      });
  }

  render() {
    const { show, booker, onClose } = this.props;
    const { privileges } = this.state;
    return (
      <Modal open={show} onClose={onClose} size="small">
        <Modal.Header>
          Booker details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h4>Username:</h4>
            {booker.username}
            <h4>Add privileges</h4>
            <Dropdown
              placeholder="Privilege"
              selection
              onChange={this.handleDropdownChange}
              options={privileges}
            />
            <Button onClick={this.handleAddPrivilegeClick}>Add Privilege</Button>
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
