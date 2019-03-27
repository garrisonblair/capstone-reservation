import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, Divider, Table, Checkbox,
} from 'semantic-ui-react';
import { DateRangePicker } from 'react-dates';
import moment from 'moment';
import api from '../../../utils/api';
import './RoomModal.scss';

class RoomModal extends Component {
  state = {
    roomID: '',
    roomCapacity: 1,
    numOfComputers: 0,
    unavailableStart: moment(),
    unavailableEnd: moment(),
    unavailableStartTime: '',
    unavailableEndTime: '',
    unavailableFocus: null,
    availabilities: [],
    hasTv: false,
    hasWindows: false,
    maxBookingDuration: '',
    maxRecurringBookingDuration: '',
    cardReader: '',
  }

  componentDidMount() {
    const { selectedRoom } = this.props;
    if (selectedRoom != null) {
      const uStart = selectedRoom.unavailable_start_time ? null : moment(selectedRoom.unavailable_start_time, 'YYYY-MM-DD HH:mm');
      const uEnd = selectedRoom.unavailable_end_time ? null : moment(selectedRoom.unavailable_end_time, 'YYYY-MM-DD HH:mm');
      this.setState({
        roomID: selectedRoom.name,
        roomCapacity: selectedRoom.capacity,
        numOfComputers: selectedRoom.number_of_computers,
        unavailableStart: uStart ? moment() : uStart,
        unavailableEnd: uEnd ? moment() : uEnd,
        unavailableStartTime: uStart ? '' : uStart.format('HH:mm'),
        unavailableEndTime: uEnd ? '' : uEnd.format('HH:mm'),
        hasTv: selectedRoom.has_tv,
        hasWindows: selectedRoom.has_windows,
        cardReader: '',
        maxBookingDuration: selectedRoom.max_booking_duration,
        maxRecurringBookingDuration: selectedRoom.max_recurring_booking_duration,
      });
    }

    this.getUnavailabilities();

    api.getCardReaders(selectedRoom ? selectedRoom.id : null)
      .then((response) => {
        if (response.data.length > 0) {
          this.setState({
            cardReader: response.data[0],
          });
        }
      });
  }

  getUnavailabilities = () => {
    const { selectedRoom } = this.props;
    api.getRoomAvailabilities(selectedRoom ? selectedRoom.id : null)
      .then((r) => {
        this.setState({ availabilities: r.data });
      });
  }

  verifyModalForm = () => {
    const {
      roomID,
      roomCapacity,
      numOfComputers,
      maxBookingDuration,
      maxRecurringBookingDuration,
    } = this.state;

    let result = true;

    if (roomID.length === 0) {
      sweetAlert('Blocked', '"Room ID" field should not be empty.', 'warning');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(roomCapacity)) {
      sweetAlert('Blocked', '"Room capacity" field should be a number.', 'warning');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(numOfComputers)) {
      sweetAlert('Blocked', '"Number of Computers" field should be a number.', 'warning');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(maxBookingDuration) && maxBookingDuration !== '') {
      sweetAlert('Blocked', '"Maximum Booking Duration" field should be a number.');
      result = false;
      // eslint-disable-next-line no-restricted-globals
    } else if (isNaN(maxRecurringBookingDuration) && maxBookingDuration !== '') {
      sweetAlert('Blocked', '"Maximum Recurring Booking Duration" field should be a number.');
      result = false;
    }

    return result;
  }

  handleRoomIdOnChange = (event) => {
    this.setState({ roomID: event.target.value });
  }

  handleRoomCapacityOnChange = (event) => {
    this.setState({ roomCapacity: event.target.value });
  }

  handleNumberOfComputersOnChange = (event) => {
    this.setState({ numOfComputers: event.target.value });
  }

  handleHasTvChange = (event, data) => {
    this.setState({ hasTv: data.checked });
  }

  handleHasWindowsChange = (event, data) => {
    this.setState({ hasWindows: data.checked });
  }

  handleBookingDurationChange = (event) => {
    this.setState({ maxBookingDuration: event.target.value });
  }

  handleRecurringBookingDurationChange = (event) => {
    this.setState({ maxRecurringBookingDuration: event.target.value });
  }

  handleSubmit = () => {
    // eslint-disable-next-line object-curly-newline
    const {
      roomID,
      roomCapacity,
      numOfComputers,
      hasTv,
      hasWindows,
    } = this.state;

    let {
      maxBookingDuration,
      maxRecurringBookingDuration,
    } = this.state;
    const { selectedRoom, onClose } = this.props;
    // Leaves the method if verification doesn't succeed
    if (!this.verifyModalForm()) {
      return;
    }

    if (maxBookingDuration === '') {
      maxBookingDuration = undefined;
    }

    if (maxRecurringBookingDuration === '') {
      maxRecurringBookingDuration = undefined;
    }

    if (selectedRoom == null) {
      api.createRoom(
        roomID,
        roomCapacity,
        numOfComputers,
        hasTv,
        hasWindows,
        maxBookingDuration,
        maxRecurringBookingDuration,
      )
        .then((response) => {
          if (response.status === 201) {
            sweetAlert('Completed', `Room '${roomID}' was successfully created.`, 'success')
              .then(() => {
                onClose();
              });
          }
        })
        .catch(() => {
          sweetAlert(':(', 'We are sorry. Something went wrong. Room was not saved.', 'error')
            .then(() => {
              onClose();
            });
        });
    } else {
      api.updateRoom(
        selectedRoom.id,
        roomID,
        roomCapacity,
        numOfComputers,
        hasTv,
        hasWindows,
        maxBookingDuration,
        maxRecurringBookingDuration,
      )
        .then((response) => {
          if (response.status === 200) {
            sweetAlert('Completed', `Room '${roomID}' was successfully updated.`, 'success')
              .then(() => {
                onClose();
              });
          }
        })
        .catch((error) => {
          sweetAlert.fire({
            position: 'top',
            type: 'error',
            title: 'Operation failed',
            text: error.response.data,
          });
        });
    }
  }

  addUnavailability = () => {
    const {
      unavailableStart,
      unavailableEnd,
      unavailableStartTime,
      unavailableEndTime,
    } = this.state;
    const { selectedRoom } = this.props;
    const unavailabilityStart = unavailableStartTime === '' ? null : `${unavailableStart.format('YYYY-MM-DD')} ${unavailableStartTime}`;
    const unavailabilityEnd = unavailableEndTime === '' ? null : `${unavailableEnd.format('YYYY-MM-DD')} ${unavailableEndTime}`;
    // Leaves the method if verification doesn't succeed
    if (!this.verifyModalForm()) {
      return;
    }
    const data = {
      room: selectedRoom.id,
      start_time: unavailabilityStart,
      end_time: unavailabilityEnd,
    };
    api.addRoomAvailability(data)
      .then((response) => {
        if (response.status === 201) {
          sweetAlert.fire({
            position: 'top',
            type: 'success',
            title: 'Time added',
            toast: true,
            showConfirmButton: false,
            timer: 2000,
          });
          this.getUnavailabilities();
        }
      })
      .catch((error) => {
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Operation failed',
          text: error.response.data,
        });
      });
  }

  deleteUnavailability = (id) => {
    api.deleteRoomAvailability(id)
      .then((response) => {
        if (response.status === 204) {
          sweetAlert.fire({
            position: 'top',
            type: 'success',
            title: 'Time removed',
            toast: true,
            showConfirmButton: false,
            timer: 2000,
          });
          this.getUnavailabilities();
        }
      })
      .catch((error) => {
        sweetAlert.fire({
          position: 'top',
          type: 'error',
          title: 'Operation failed',
          text: error.response.data,
        });
      });
  }

  handleCardReaderDelete = () => {
    const { cardReader } = this.state;
    api.deleteCardReader(cardReader.id)
      .then(() => {
        this.setState({ cardReader: undefined });
      })
      .catch(() => {
        sweetAlert(':(', 'Card reader could not be deleted', 'error');
      });
  }

  handleGenerateCardReaderKey = () => {
    const { selectedRoom } = this.props;
    api.createCardReader(selectedRoom.id)
      .then((response) => {
        this.setState({ cardReader: response.data });
      })
      .catch(() => {
        sweetAlert(':(', 'Card reader key could not be generated', 'error');
      });
  }

  handleTime = (e) => {
    if (e.target.id === 'start') {
      this.setState({ unavailableStartTime: e.target.value });
    } else {
      this.setState({ unavailableEndTime: e.target.value });
    }
  }

  renderCardReader = () => {
    const { cardReader } = this.state;

    return (
      <div>
        <h3>
          Card Reader UUID:
        </h3>
        <div>
          <Input
            className="uuid_field"
            value={cardReader.secret_key}
          />
          <Button
            className="cardReaderDelete"
            onClick={this.handleCardReaderDelete}
          >
            Delete
          </Button>
        </div>
      </div>
    );
  }

  renderAvailability = () => {
    const {
      unavailableEnd,
      unavailableStart,
      unavailableEndTime,
      unavailableStartTime,
      unavailableFocus,
      availabilities,
    } = this.state;
    const { selectedRoom } = this.props;
    const a = [];
    availabilities.forEach((av) => {
      if (av.room === selectedRoom.id) {
        const start = av.start_time.split('T');
        const end = av.end_time.split('T');
        const text = `${start[0]} to ${end[0]}, ${start[1].substring(0, 5)} to ${end[1].substring(0, 5)}`;
        a.push(
          <div key={av.id}>
            {text}
            &emsp;
            <input type="button" value="Delete" onClick={() => this.deleteUnavailability(av.id)} />
          </div>,
        );
      }
    });
    return (
      <div>
        {a}
        <FormField>
          <DateRangePicker
            startDate={unavailableStart}
            startDateId="start_date_id"
            endDate={unavailableEnd}
            endDateId="end_date_id"
            onDatesChange={({ startDate, endDate }) => this.setState({
              unavailableStart: startDate,
              unavailableEnd: endDate,
            })}
            focusedInput={unavailableFocus}
            onFocusChange={f => this.setState({ unavailableFocus: f })}
          />
          <br />
          Start time:&nbsp;
          <input type="time" id="start" defaultValue={unavailableStartTime} onChange={e => this.handleTime(e)} />
          <br />
          End time:&nbsp;
          <input type="time" id="end" defaultValue={unavailableEndTime} onChange={e => this.handleTime(e)} />
          <br />
          <Button primary content="Add" onClick={() => this.addUnavailability()} />
        </FormField>
      </div>
    );
  }

  renderCreateCardReader = () => (
    <Button onClick={this.handleGenerateCardReaderKey}>
      Generate Card Reader Key
    </Button>
  );

  render() {
    const { show, onClose, selectedRoom } = this.props;
    const {
      roomCapacity,
      roomID,
      numOfComputers,
      hasTv,
      hasWindows,
      cardReader,
      maxBookingDuration,
      maxRecurringBookingDuration,
    } = this.state;

    return (
      <Modal centered={false} size="small" open={show} id="room-modal" onClose={onClose}>
        <Modal.Header>
          Room Details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h3>Room:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleRoomIdOnChange}
                value={roomID}
                disabled={selectedRoom != null}
              />
            </FormField>
            <Table>
              <tbody>
                <tr>
                  <td>
                    <h3>Room capacity:</h3>
                    <FormField>
                      <Input
                        size="small"
                        onChange={this.handleRoomCapacityOnChange}
                        value={roomCapacity}
                      />
                    </FormField>
                  </td>
                  <td>
                    <h3>Number of computers:</h3>
                    <FormField>
                      <Input
                        size="small"
                        onChange={this.handleNumberOfComputersOnChange}
                        value={numOfComputers}
                      />
                    </FormField>
                  </td>
                </tr>
                <tr>
                  <td>
                    <h3>Has TV:</h3>
                    <FormField>
                      <Checkbox
                        checked={hasTv}
                        onChange={this.handleHasTvChange}
                      />
                    </FormField>
                  </td>
                  <td>
                    <h3>Has Windows:</h3>
                    <FormField>
                      <Checkbox
                        checked={hasWindows}
                        onChange={this.handleHasWindowsChange}
                      />
                    </FormField>
                  </td>
                </tr>
              </tbody>
            </Table>
            <Divider />
            <h3>Maximum duration of Booking (Hours):</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleBookingDurationChange}
                value={maxBookingDuration === null ? '' : maxBookingDuration}
              />
            </FormField>
            <h3>Maximum duration of Recurring Bookings (Hours):</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleRecurringBookingDurationChange}
                value={maxRecurringBookingDuration === null ? '' : maxRecurringBookingDuration}
              />
            </FormField>
            <Divider />
            <h3>Unavailabilities:</h3>
            <br />
            { this.renderAvailability() }
            <Divider />
            <FormField>
              { cardReader ? this.renderCardReader() : this.renderCreateCardReader()}
            </FormField>
            <br />
            <br />
            <Button onClick={this.handleSubmit} color="blue">SAVE</Button>
            <Button onClick={onClose}>Close</Button>
          </Modal.Description>
        </Modal.Content>
      </Modal>
    );
  }
}

RoomModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  selectedRoom: PropTypes.shape({
    id: PropTypes.number,
    name: PropTypes.string,
    capacity: PropTypes.number,
    number_of_computers: PropTypes.number,
    has_tv: PropTypes.bool,
    has_windows: PropTypes.bool,
    maxBookingDuration: PropTypes.number,
    maxRecurringBookingDuration: PropTypes.number,
  }),
};

RoomModal.defaultProps = {
  selectedRoom: null,
};


export default RoomModal;
