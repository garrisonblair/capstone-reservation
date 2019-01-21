import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Form, Input, Button, Icon, Step, Loader,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './ResetPassword.scss';


class ResetPassword extends Component {
  state = {
    username: '',
    modalType: 'info',
    showLoader: false,
  };

  componentWillMount() {
    const { showLoaderForTest } = this.props;
    // This is only for testing.
    if (showLoaderForTest) {
      this.setState({ showLoader: true });
    }
  }

  handleUsername = (event) => {
    this.setState({ username: event.target.value });
  }

  closeModal = () => {
    const { modalType } = this.state;
    // eslint-disable-next-line react/prop-types
    const { history } = this.props;
    if (modalType === 'success') {
      history.push('/');
    }
  }

  sendEmail = () => {
    const { username } = this.state;

    this.setState({ showLoader: true });

    api.resetPassword(username)
      .then((response) => {
        if (response.status === 201) {
          this.setState({
            showLoader: false,
          });
          sweetAlert(
            'A link for reset password has been sent to your email account.',
            'Please click on the link to continue the reset password process.',
            'success',
          );
        }
      })
      .catch((error) => {
        this.setState({ showLoader: false });
        if (error.message.includes('400')) {
          sweetAlert(
            'User does not exist',
            "We couldn't find this user in the system.",
            'error',
          );
        }
      });
  }

  renderMainForm() {
    return (
      <div>
        <h1>Reset Password</h1>
        <Step.Group size="mini" widths={2}>
          <Step active>
            <Icon name="envelope" />
            <Step.Content>
              <Step.Title>Step 1</Step.Title>
              <Step.Description>Username confirmation</Step.Description>
            </Step.Content>
          </Step>
          <Step>
            <Icon name="cog" />
            <Step.Content>
              <Step.Title>Step 2</Step.Title>
              <Step.Description>Reset Password</Step.Description>
            </Step.Content>
          </Step>
        </Step.Group>
        <p>Please enter your username. A confirmation will be sent to your email.</p>
        <Form.Field>
          <Input
            fluid
            size="small"
            icon="user"
            iconPosition="left"
            placeholder="ex. a_test"
            onChange={this.handleUsername}
          />
        </Form.Field>
        <Form.Field>
          <br />
          <Button fluid size="small" icon onClick={this.sendEmail}>
            Send Email
          </Button>
        </Form.Field>
      </div>
    );
  }

  render() {
    const { showLoader } = this.state;
    return (
      <div id="resetPassword">
        <div className="container">
          {showLoader ? <Loader active inline="centered" size="large" /> : this.renderMainForm()}
        </div>
      </div>
    );
  }
}

ResetPassword.propTypes = {
  showLoaderForTest: PropTypes.bool,
};

ResetPassword.defaultProps = {
  showLoaderForTest: false,
};

export default ResetPassword;
