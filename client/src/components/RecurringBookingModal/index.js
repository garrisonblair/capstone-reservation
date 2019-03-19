import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
  Form,
  Input,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';


class RecurringBookingModal extends Component {
  state = {
    show: false,
    booking: null,
  }

  componentWillMount() {
    const { show, booking } = this.props;
    this.setState({ show, booking });
    console.log(booking);
  }

  closeModal = () => {
    const { onClose } = this.props;
    this.setState({
      show: false,
    });
    onClose();
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

  renderEdit() {
    const { booking } = this.props;
    return (
      <Form>
        <Input placeholder={booking.room} />
      </Form>
    );
  }

  render() {
    const { show } = this.state;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size="tiny" open={show} onClose={this.closeModal}>
          <Modal.Header>
            Recurring booking
          </Modal.Header>
          <Modal.Content>
            {this.renderEdit()}
          </Modal.Content>
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
