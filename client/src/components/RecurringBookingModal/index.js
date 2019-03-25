/* eslint-disable camelcase */
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Modal,
  Form,
  Input,
  Button,
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
    isLoading: false,
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

  handleEditButton = () => {
    this.sendEditRequest(null);
  }

  sendEditRequest = (skipConflicts) => {
    const {
      room,
      start_date,
      end_date,
      booking_start_time,
      booking_end_time,
    } = this.state;
    const { booking } = this.props;
    const data = {
      room,
      start_date: start_date.format('YYYY-MM-DD'),
      end_date: end_date.format('YYYY-MM-DD'),
      booking_start_time,
      booking_end_time,
      skip_conflicts: skipConflicts,
    };
    this.setState({ isLoading: true });
    api.editRecurringBooking(data, booking.id)
      .then((response) => {
        this.setState({ isLoading: false });
        let conflictsMessage = '';
        if (response.data.length > 0) {
          conflictsMessage = 'Except for:<ul>';
          // eslint-disable-next-line no-return-assign
          response.data.map(date => conflictsMessage = `${conflictsMessage}<li>${date}</li>`);
          conflictsMessage = `${conflictsMessage}</ul>`;
        }
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          html: `Recurring booking was updated.<br/><div id="exception-dates">${conflictsMessage}</div>`,
        })
          .then(() => {
            this.closeModal();
          });
      })
      .catch((error) => {
        this.setState({ isLoading: false });

        if (error.status === 409) {
          sweetAlert.fire({
            position: 'top',
            type: 'warning',
            title: 'Conflicts detected',
            html: `There are booking overlapping with other reservations. Skip edit on these dates or cancel edit?<br/><br/><div><center>${error.data}</center></div>`,
            confirmButtonText: 'Skip',
            cancelButtonText: 'Cancel',
            showCancelButton: true,
          })
            .then((r) => {
              if (r.value) {
                this.sendEditRequest(true);
              }
            });
        } else {
          sweetAlert.fire({
            position: 'top',
            type: 'error',
            title: 'Edit failed',
            text: error.data,
          });
        }
      });
  }

  handleDeleteButton = () => {
    const { booking } = this.props;
    sweetAlert.fire({
      position: 'top',
      type: 'warning',
      text: 'This will delete all bookings associated with this recurring booking.',
      confirmButtonText: 'Confirm',
      cancelButtonText: 'Cancel',
      showCancelButton: true,
    })
      .then((r) => {
        if (r.value) {
          this.setState({ isLoading: true });
          api.deleteRecurringBooking(booking.id)
            .then(() => {
              this.setState({ isLoading: false });
              this.closeModal();
              sweetAlert.fire({
                position: 'top',
                type: 'success',
                title: 'Recurring booking was successfully deleted.',
                toast: true,
                showConfirmButton: false,
                timer: 2000,
              });
            })
            .catch((error) => {
              this.setState({ isLoading: false });

              sweetAlert.fire({
                position: 'top',
                type: 'error',
                text: error.response.data,
              });
            });
        }
      });
  }

  handleOpen = () => this.setState({ show: true });

  handleTime = (e) => {
    if (e.target.id === 'start') {
      this.setState({ booking_start_time: e.target.value });
    } else {
      this.setState({ booking_end_time: e.target.value });
    }
  }

  formatTime = (e) => {
    const { booking_start_time, booking_end_time } = this.state;
    const t = e.target.id === 'start' ? booking_start_time : booking_end_time;
    const time = t.split(':');
    time[1] = parseInt(time[1], 10);
    time[1] -= time[1] % 10;
    if (parseInt(time[0], 10) < 10) {
      time[0] = '09';
    }
    if (parseInt(time[0], 10) > 23) {
      time[0] = '23';
    }
    if (e.target.id === 'start') {
      this.setState({ booking_start_time: `${time[0]}:${time[1] < 10 ? '00' : time[1]}:00` });
    } else {
      this.setState({ booking_end_time: `${time[0]}:${time[1] < 10 ? '00' : time[1]}:00` });
    }
  }

  renderEdit() {
    const {
      focus,
      room,
      start_date,
      end_date,
      booking_start_time,
      booking_end_time,
      group,
      isLoading,
    } = this.state;
    return (
      <Form>
        <Form.Field>
          Room:&nbsp;
          {room}
        </Form.Field>
        <Form.Field>
          Date range:&nbsp;
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
        </Form.Field>
        <Form.Field>
          Start time:
          <input type="time" id="start" min="9:00" max="23:00" value={booking_start_time} onChange={e => this.handleTime(e)} onBlur={e => this.formatTime(e)} />
        </Form.Field>
        <Form.Field>
          End time:
          <input type="time" id="end" min="9:00" max="23:00" value={booking_end_time} onChange={e => this.handleTime(e)} onBlur={e => this.formatTime(e)} />
        </Form.Field>
        <Button className="edit-button" color="blue" loading={isLoading} onClick={this.handleEditButton}>Apply changes</Button>
        <div className="ui divider" />
        <Button className="delete-button" color="red" onClick={this.handleDeleteButton}>Delete all bookings</Button>
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
