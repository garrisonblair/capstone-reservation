import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import api from '../../utils/api';
import storage from '../../utils/local-storage';


function AdminRequired(InnerComponent) {
  class HOC extends Component {
    componentDidMount() {
      const { history } = this.props;

      if (!storage.getUser()) {
        history.push('/404');
        return;
      }

      api.getMyUser()
        .then((response) => {
          const { data } = response;
          if (!data.is_superuser) {
            history.push('/404');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.log(error);
        });
    }

    render() {
      return <InnerComponent {...this.props} />;
    }
  }

  return withRouter(HOC);
}

export default AdminRequired;
