import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Modal } from 'semantic-ui-react';

class BookerModal extends Component {
  state = {
    // eslint-disable-next-line react/no-unused-state
    bookerName: '',
  }

  render() {
    const { show, booker, onClose } = this.props;
    return (
      <Modal open={show} onClose={onClose}>
        <Modal.Header>
          Booker details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h4>Username:</h4>
            {booker.username}
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
