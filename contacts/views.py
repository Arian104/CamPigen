from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Contact
from organizations.models import Organization, OrganizationMembership

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simple_create_contact(request):
    try:
        data = request.data
        email = data.get('email')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        org_id = data.get('organization_id')
        
        # Get organization
        if org_id:
            try:
                organization = Organization.objects.get(id=org_id)
            except Organization.DoesNotExist:
                return Response({'error': 'Invalid organization ID'}, status=status.HTTP_400_BAD_REQUEST)
        elif hasattr(request.user, 'active_organization') and request.user.active_organization:
            organization = request.user.active_organization
        else:
            return Response({'error': 'No organization specified'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission
        if not request.user.is_superuser:
            is_member = OrganizationMembership.objects.filter(
                user=request.user, 
                organization=organization
            ).exists()
            if not is_member:
                return Response({'error': 'You are not a member of this organization'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if contact already exists
        existing = Contact.objects.filter(email=email, organization=organization).first()
        if existing:
            return Response({
                'error': 'Contact already exists',
                'id': str(existing.id)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        contact = Contact.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            organization=organization
        )
        
        return Response({
            'id': str(contact.id),
            'email': contact.email,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'message': 'Contact created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_contacts(request):
    user = request.user
    
    if user.is_superuser:
        contacts = Contact.objects.all()
    else:
        user_orgs = OrganizationMembership.objects.filter(user=user).values_list('organization_id', flat=True)
        contacts = Contact.objects.filter(
            models.Q(organization__in=user_orgs) | models.Q(organization=None)
        )
    
    contacts_list = [{
        'id': str(c.id),
        'email': c.email,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'organization_name': c.organization.name if c.organization else 'Global'
    } for c in contacts]
    
    return Response(contacts_list, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_contacts(request):
    """Get all contacts - public for testing"""
    contacts = Contact.objects.all()
    contacts_list = [{
        'id': str(c.id),
        'email': c.email,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'organization_id': str(c.organization.id) if c.organization else None
    } for c in contacts]
    return Response(contacts_list, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_global_contacts(request):
    """Get global contacts only"""
    contacts = Contact.objects.filter(organization=None)
    contacts_list = [{
        'id': str(c.id),
        'email': c.email,
        'first_name': c.first_name,
        'last_name': c.last_name
    } for c in contacts]
    return Response(contacts_list, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_organizations(request):
    orgs = Organization.objects.all()
    orgs_list = [{
        'id': str(org.id),
        'name': org.name,
        'subdomain': org.subdomain
    } for org in orgs]
    return Response(orgs_list, status=status.HTTP_200_OK)
