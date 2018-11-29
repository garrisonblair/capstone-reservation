import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Form, Modal, Header,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';


class DisableBackupModal extends Component {
  disableBackup = () => {
    const { onClose } = this.props;
    const data = {
      is_webcalendar_backup_active: false,
    };

    api.updateAdminSettings(data)
      .then(() => {
        sweetAlert(
          'Completed',
          'Settings were successfully saved.',
          'success',
        );
        onClose();
      })
      .catch((error) => {
        // eslint-disable-next-line no-console
        console.log(error);
      });
  }

  render() {
    const { show } = this.props;
    return (
      <Modal open={show}>
        <Header>
          <h1 className="login__container__header__title">
            {'Disable automatic backup?'}
          </h1>
        </Header>
        <div className="login__container__main">
          <div className="ui divider" />
          <div className="login__container__main__form-wrapper">
            <Form.Field>
              <Button fluid size="small" icon onClick={this.disableBackup}>
                Confirm
              </Button>
            </Form.Field>
            <div className="ui divider" />
          </div>
        </div>
      </Modal>
    );
  }
}

DisableBackupModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default DisableBackupModal;
