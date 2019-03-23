import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Header, Icon, Modal,
} from 'semantic-ui-react';
import './PrivilegeDetailsModal.scss';


class PrivilegeDetailsModal extends Component {
  renderBoolean = (boolean, inherited) => (
    <div className="privilege_bool">
      <Icon
        name={boolean ? 'check circle' : 'times circle'}
        color={boolean ? 'green' : 'red'}
      />
      { inherited ? '(Inherited)' : null }
    </div>
  )

  render() {
    const { show, onClose, privilege } = this.props;
    if (privilege.name) {
      console.log(privilege);
      return (
        <Modal className="privilege-details-modal" open={show} onClose={onClose}>
          <Header>
            {privilege.name}
          </Header>
          <div className="privilege-details-modal__container">
            <p>
              <strong> Name: </strong>
              {privilege.name}
            </p>
            <p>
              <strong> Default: </strong>
              {this.renderBoolean(privilege.is_default)}
            </p>
            <p>
              <strong> Parent Category: </strong>
              {privilege.parent_category ? privilege.parent_category.name : '-'}
            </p>
            <p>
              <strong> Related Course: </strong>
              {privilege.related_course || '-'}
            </p>
            <p>
              <strong> Max Days Until Booking: </strong>
              {privilege.max_days_until_booking !== null ? privilege.max_days_until_booking : `${privilege.inherited_values.max_days_until_booking} (Inherited)`}
            </p>
            <p>
              <strong> Max Bookings per day: </strong>
              {privilege.max_num_bookings_for_date !== null ? privilege.max_num_bookings_for_date : `${privilege.inherited_values.max_num_bookings_for_date} (Inherited)`}
            </p>
            <p>
              <strong> Max days with bookings: </strong>
              {privilege.max_num_days_with_bookings !== null ? privilege.max_num_days_with_bookings : `${privilege.inherited_values.max_num_days_with_bookings} (Inherited)`}
            </p>
            <p>
              <strong> Max Recurring Bookings: </strong>
              {privilege.max_recurring_bookings !== null ? privilege.max_recurring_bookings : `${privilege.inherited_values.max_recurring_bookings} (Inherited)`}
            </p>
            <p>
              <strong> Recurring Booking Permission: </strong>
              {privilege.booking_start_time !== null ? this.renderBoolean(privilege.can_make_recurring_booking)
                : this.renderBoolean(privilege.inherited_values.can_make_recurring_booking, true)}
            </p>
            <p>
              <strong> Booking Start Time: </strong>
              {privilege.booking_start_time !== null ? privilege.booking_start_time : `${privilege.inherited_values.booking_start_time} (Inherited)`}
            </p>
            <p>
              <strong> Booking End Time: </strong>
              {privilege.booking_end_time !== null ? privilege.booking_end_time : `${privilege.inherited_values.booking_end_time} (Inherited)`}
            </p>
          </div>
          <div className="ui divider" />
          <div className="controls">
            <Button icon labelPosition="left" negative size="small" onClick={onClose}>
              <Icon name="x" />
              Close
            </Button>
          </div>
        </Modal>
      );
    }
    return null;
  }
}

PrivilegeDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  privilege: PropTypes.object.isRequired,
};


export default PrivilegeDetailsModal;
