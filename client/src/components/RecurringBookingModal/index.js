/* eslint-disable camelcase */
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
  Form,
  Input,
} from 'semantic-ui-react';
import { DateRangePicker } from 'react-dates';
import sweetAlert from 'sweetalert2';
import moment from 'moment';
import api from '../../utils/api';


class RecurringBookingModal extends Component {
  state = {
    show: false,
    focus: null,
    room: '',
    start_date: null,
    end_date: null,
    booking_start_time: '',
    booking_end_time: '',
    group: '',

  }

  componentWillMount() {
    const { show, booking } = this.props;
    this.setState({
      show,
      room: booking.room.name,
      start_date: moment(booking.start_date, 'YYYY-MM-DD'),
      end_date: moment(booking.end_date, 'YYYY-MM-DD'),
      booking_start_time: booking.booking_start_time,
      booking_end_time: booking.booking_end_time,
      group: booking.group,
    });
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
    const {
      focus,
      room,
      start_date,
      end_date,
      booking_start_time,
      booking_end_time,
      group,
    } = this.state;
    return (
      <Form>
        Room
        <Input placeholder={room} />
        <DateRangePicker
          startDate={start_date}
          startDateId="sId"
          endDate={end_date}
          endDateId="eId"
          onDatesChange={({ startDate, endDate }) => (this.setState({
            start_date: startDate,
            end_date: endDate,
          }))}
          focusedInput={focus}
          onFocusChange={f => this.setState({ focus: f })}
        />
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
