import React, { Component } from 'react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';


function AuthenticationRequired(InnerComponent) {
  class HOC extends Component {
    componentDidMount() {
      // eslint-disable-next-line react/prop-types
      const { history } = this.props;

      if (!storage.getUser()) {
        history.push('/');
        return;
      }

      api.getUser(storage.getUser().id)
        .then((response) => {
          const { data } = response;
          if (!data) {
            history.push('/');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.log(error);
          history.push('/');
        });
    }

    render() {
      return <InnerComponent {...this.props} />;
    }
  }

  return HOC;
}

export default AuthenticationRequired;
