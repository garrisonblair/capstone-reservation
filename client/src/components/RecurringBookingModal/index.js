import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';


class RecurringBookingModal extends Component {
  state = {
    show: false,
  }

  componentWillMount() {
    const { show } = this.props;
    this.setState({ show });
  }

  closeModal = () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
  }

  // Close the modal if any api POST requests succeeded
  closeModalWithAction = () => {
    const { onCloseWithAction } = this.props;
    this.setState({
      show: false,
    });
    onCloseWithAction();
  }

  handleOpen = () => this.setState({ show: true });

  render() {
    const { show } = this.state;
    const { booking } = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size="tiny" open={show} onClose={this.closeModal}>
          <Modal.Header>
            Recurring booking
          </Modal.Header>
        </Modal>
      </div>
    );
  }
}

RecurringBookingModal.propTypes = {
  show: PropTypes.bool.isRequired,
  booking: PropTypes.instanceOf(Object).isRequired,
  onClose: PropTypes.func,
  onCloseWithAction: PropTypes.func,
};

RecurringBookingModal.defaultProps = {
  onClose: () => { },
  onCloseWithAction: () => { },
};

export default RecurringBookingModal;
