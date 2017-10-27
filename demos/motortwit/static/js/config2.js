(function () {
    "use strict";
    var onSubmitError = function(error, form, progression, notification) {
            // mark fields based on errors from the response
            if (!('error_details' in error.data)){
                return true;
            }
            _.mapObject(error.data.error_details, function(error_msg, field_name) {
                if (form[field_name]) {
                    form[field_name].$valid = false;
                }
                return {}
            });
            // stop the progress bar
            progression.done();
            // add a notification
            notification.log(`Some values are invalid, see details in the form`,
                             { addnCls: 'humane-flatty-error' });
            // cancel the default action (default error messages)
            return false;
        }

    var app = angular.module('aiohttp_admin', ['ng-admin']);
    app.config(['RestangularProvider', function(RestangularProvider) {
        var token = window.localStorage.getItem('aiohttp_admin_token');
        RestangularProvider.setDefaultHeaders({'Authorization': token});
    }]);

    app.config(['NgAdminConfigurationProvider', function (NgAdminConfigurationProvider) {
        var nga = NgAdminConfigurationProvider;

        var admin = nga.application("aiohttp_admin")
            .debug(true)
            .baseApiUrl('/admin/');

        admin.errorMessage(function (response) {
            var msg = '<p>Oops error occured with status code: ' + response.status + '</p>\n';

            if ('error_details' in response.data ){
                msg += '<code>';
                msg += JSON.stringify(response.data.error_details, null, 2);
                msg += '</code>';
            }
            return msg;
        });

        var user = nga.entity('user').identifier(nga.field('_id'));
        var message = nga.entity('message').identifier(nga.field('_id'));
        var follower = nga.entity('follower').identifier(nga.field('_id'));
        
        admin.addEntity(user);
        admin.addEntity(message);
        admin.addEntity(follower);
        
        
    user.listView()
        .title('List entity user')
        .description('List of user')
        .perPage(50)
        .fields([
            nga.field('_id', 'string').isDetailLink(true),
        ])
        .sortField('_id')
        .listActions(['show', 'edit', 'delete']);

            
    user.creationView()
        .title('Create entity user')
        .fields([
            nga.field('pw_hash', 'string'),
            nga.field('email', 'string'),
            nga.field('username', 'string'),
            
        ]);
    user.creationView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    user.editionView()
        .title('Edit entity user')
        .fields([
            nga.field('_id', 'string').editable(false),
            nga.field('pw_hash', 'string'),
            nga.field('email', 'string'),
            nga.field('username', 'string'),
        ]);
    user.editionView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    user.showView()
        .title('Show entity user')
        .fields([
            nga.field('pw_hash', 'string'),
            nga.field('email', 'string'),
            nga.field('_id', 'string'),
            nga.field('username', 'string'),
            
        ]);

            
    user.deletionView()
        .title('Deletion confirmation for entity user');

        
    message.listView()
        .title('List entity message')
        .description('List of message')
        .perPage(50)
        .fields([
            nga.field('_id', 'string').isDetailLink(true),
        ])
        .sortField('_id')
        .listActions(['show', 'edit', 'delete']);

            
    message.creationView()
        .title('Create entity message')
        .fields([
            nga.field('username', 'string'),
            nga.field('pub_date', 'datetime'),
            nga.field('author_id', 'string'),
            nga.field('text', 'string'),
            
        ]);
    message.creationView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    message.editionView()
        .title('Edit entity message')
        .fields([
            nga.field('_id', 'string').editable(false),
            nga.field('username', 'string'),
            nga.field('pub_date', 'datetime'),
            nga.field('author_id', 'string'),
            nga.field('text', 'string'),
        ]);
    message.editionView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    message.showView()
        .title('Show entity message')
        .fields([
            nga.field('username', 'string'),
            nga.field('pub_date', 'datetime'),
            nga.field('_id', 'string'),
            nga.field('author_id', 'string'),
            nga.field('text', 'string'),
            
        ]);

            
    message.deletionView()
        .title('Deletion confirmation for entity message');

        
    follower.listView()
        .title('List entity follower')
        .description('List of follower')
        .perPage(50)
        .fields([
            nga.field('_id', 'string').isDetailLink(true),
        ])
        .sortField('_id')
        .listActions(['show', 'edit', 'delete']);

            
    follower.creationView()
        .title('Create entity follower')
        .fields([
            nga.field('who_id', 'string'),
            nga.field('whom_id', 'json'),
            
        ]);
    follower.creationView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    follower.editionView()
        .title('Edit entity follower')
        .fields([
            nga.field('_id', 'string').editable(false),
            nga.field('who_id', 'string'),
            nga.field('whom_id', 'json'),
        ]);
    follower.editionView()
        .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

            
    follower.showView()
        .title('Show entity follower')
        .fields([
            nga.field('who_id', 'string'),
            nga.field('_id', 'string'),
            nga.field('whom_id', 'json'),
            
        ]);

            
    follower.deletionView()
        .title('Deletion confirmation for entity follower');

        

        nga.configure(admin);
    }]);

}());